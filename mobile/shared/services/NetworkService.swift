import Foundation
import Combine

// MARK: - Network Service Protocol
protocol NetworkServiceProtocol {
    func request<T: Codable>(_ endpoint: APIEndpoint) -> AnyPublisher<T, NetworkError>
    func upload<T: Codable>(_ endpoint: APIEndpoint, data: Data, progress: @escaping (Double) -> Void) -> AnyPublisher<T, NetworkError>
    func download(_ endpoint: APIEndpoint, progress: @escaping (Double) -> Void) -> AnyPublisher<Data, NetworkError>
}

// MARK: - Network Service Implementation
class NetworkService: NetworkServiceProtocol {
    private let session: URLSession
    private let baseURL: URL
    private let authManager: AuthManagerProtocol
    private let requestQueue = DispatchQueue(label: "com.addisababa.aischool.network", qos: .utility)
    
    init(session: URLSession = .shared, baseURL: URL, authManager: AuthManagerProtocol) {
        self.session = session
        self.baseURL = baseURL
        self.authManager = authManager
    }
    
    func request<T: Codable>(_ endpoint: APIEndpoint) -> AnyPublisher<T, NetworkError> {
        guard let request = createRequest(for: endpoint) else {
            return Fail(error: NetworkError.invalidRequest)
                .eraseToAnyPublisher()
        }
        
        return session.dataTaskPublisher(for: request)
            .tryMap { data, response in
                try self.handleResponse(data: data, response: response)
            }
            .decode(type: T.self, decoder: JSONDecoder())
            .mapError { error in
                if let networkError = error as? NetworkError {
                    return networkError
                }
                return NetworkError.decodingError(error)
            }
            .eraseToAnyPublisher()
    }
    
    func upload<T: Codable>(_ endpoint: APIEndpoint, data: Data, progress: @escaping (Double) -> Void) -> AnyPublisher<T, NetworkError> {
        guard var request = createRequest(for: endpoint) else {
            return Fail(error: NetworkError.invalidRequest)
                .eraseToAnyPublisher()
        }
        
        request.httpMethod = "POST"
        request.setValue("multipart/form-data", forHTTPHeaderField: "Content-Type")
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"upload.data\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/octet-stream\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        return session.dataTaskPublisher(for: request)
            .tryMap { data, response in
                try self.handleResponse(data: data, response: response)
            }
            .decode(type: T.self, decoder: JSONDecoder())
            .mapError { error in
                if let networkError = error as? NetworkError {
                    return networkError
                }
                return NetworkError.decodingError(error)
            }
            .eraseToAnyPublisher()
    }
    
    func download(_ endpoint: APIEndpoint, progress: @escaping (Double) -> Void) -> AnyPublisher<Data, NetworkError> {
        guard let request = createRequest(for: endpoint) else {
            return Fail(error: NetworkError.invalidRequest)
                .eraseToAnyPublisher()
        }
        
        return session.dataTaskPublisher(for: request)
            .tryMap { data, response in
                try self.handleResponse(data: data, response: response)
            }
            .mapError { error in
                if let networkError = error as? NetworkError {
                    return networkError
                }
                return NetworkError.unknown(error)
            }
            .eraseToAnyPublisher()
    }
    
    // MARK: - Private Methods
    
    private func createRequest(for endpoint: APIEndpoint) -> URLRequest? {
        guard let url = URL(string: endpoint.path, relativeTo: baseURL) else {
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.timeoutInterval = APIConstants.timeoutInterval
        
        // Add headers
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        // Add authorization header if needed
        if endpoint.requiresAuth {
            if let token = authManager.accessToken {
                request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
            }
        }
        
        // Add custom headers
        for (key, value) in endpoint.headers {
            request.setValue(value, forHTTPHeaderField: key)
        }
        
        // Add body for POST/PUT requests
        if let body = endpoint.body {
            request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        }
        
        return request
    }
    
    private func handleResponse(data: Data, response: URLResponse) throws -> Data {
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            return data
        case 401:
            // Token expired, try to refresh
            authManager.refreshToken { [weak self] success in
                if success {
                    // Retry the request
                    // This would need to be implemented with a retry mechanism
                }
            }
            throw NetworkError.unauthorized
        case 403:
            throw NetworkError.forbidden
        case 404:
            throw NetworkError.notFound
        case 422:
            throw NetworkError.validationError(data)
        case 500...599:
            throw NetworkError.serverError
        default:
            throw NetworkError.unknown(nil)
        }
    }
}

// MARK: - API Endpoint Protocol
protocol APIEndpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var headers: [String: String] { get }
    var body: [String: Any]? { get }
    var requiresAuth: Bool { get }
}

// MARK: - HTTP Methods
enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case PATCH = "PATCH"
    case DELETE = "DELETE"
}

// MARK: - Network Errors
enum NetworkError: Error, LocalizedError {
    case invalidRequest
    case invalidResponse
    case unauthorized
    case forbidden
    case notFound
    case validationError(Data)
    case serverError
    case decodingError(Error)
    case unknown(Error?)
    
    var errorDescription: String? {
        switch self {
        case .invalidRequest:
            return "Invalid request"
        case .invalidResponse:
            return "Invalid response"
        case .unauthorized:
            return "Unauthorized access"
        case .forbidden:
            return "Access forbidden"
        case .notFound:
            return "Resource not found"
        case .validationError:
            return "Validation error"
        case .serverError:
            return "Server error"
        case .decodingError(let error):
            return "Decoding error: \(error.localizedDescription)"
        case .unknown(let error):
            return error?.localizedDescription ?? "Unknown error occurred"
        }
    }
}

// MARK: - Concrete API Endpoints

// MARK: - Authentication Endpoints
struct LoginEndpoint: APIEndpoint {
    let email: String
    let password: String
    let role: UserRole
    
    var path: String { APIConstants.Endpoints.login }
    var method: HTTPMethod { .POST }
    var headers: [String: String] { [:] }
    var body: [String: Any]? {
        [
            "email": email,
            "password": password,
            "role": role.rawValue
        ]
    }
    var requiresAuth: Bool { false }
}

struct LogoutEndpoint: APIEndpoint {
    var path: String { APIConstants.Endpoints.logout }
    var method: HTTPMethod { .POST }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
}

struct RefreshTokenEndpoint: APIEndpoint {
    let refreshToken: String
    
    var path: String { APIConstants.Endpoints.refreshToken }
    var method: HTTPMethod { .POST }
    var headers: [String: String] { [:] }
    var body: [String: Any]? {
        ["refresh_token": refreshToken]
    }
    var requiresAuth: Bool { false }
}

// MARK: - User Endpoints
struct GetUserProfileEndpoint: APIEndpoint {
    var path: String { APIConstants.Endpoints.profile }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
}

struct UpdateUserProfileEndpoint: APIEndpoint {
    let profileData: [String: Any]
    
    var path: String { APIConstants.Endpoints.profile }
    var method: HTTPMethod { .PATCH }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { profileData }
    var requiresAuth: Bool { true }
}

// MARK: - Student Endpoints
struct GetStudentsEndpoint: APIEndpoint {
    let page: Int
    let pageSize: Int
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.students }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(page: Int = 1, pageSize: Int = 20, filters: [String: Any]? = nil) {
        self.page = page
        self.pageSize = pageSize
        self.filters = filters
    }
}

struct GetStudentEndpoint: APIEndpoint {
    let studentId: String
    
    var path: String { APIConstants.Endpoints.studentProfile.replacingOccurrences(of: "{id}", with: studentId) }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
}

struct GetStudentDashboardEndpoint: APIEndpoint {
    let studentId: String
    
    var path: String { APIConstants.Endpoints.dashboard.replacingOccurrences(of: "{id}", with: studentId) }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
}

// MARK: - AI Teacher Endpoints
struct GetAILessonsEndpoint: APIEndpoint {
    let page: Int
    let pageSize: Int
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.aiLessons }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(page: Int = 1, pageSize: Int = 20, filters: [String: Any]? = nil) {
        self.page = page
        self.pageSize = pageSize
        self.filters = filters
    }
}

struct GetAILessonEndpoint: APIEndpoint {
    let lessonId: String
    
    var path: String { APIConstants.Endpoints.aiLessonDetail.replacingOccurrences(of: "{id}", with: lessonId) }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
}

// MARK: - Analytics Endpoints
struct GetLearningAnalyticsEndpoint: APIEndpoint {
    let studentId: String?
    let timeRange: TimeRange
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.learningAnalytics }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(studentId: String? = nil, timeRange: TimeRange = .week, filters: [String: Any]? = nil) {
        self.studentId = studentId
        self.timeRange = timeRange
        self.filters = filters
    }
}

// MARK: - Monitoring Endpoints
struct GetWebcamSessionsEndpoint: APIEndpoint {
    let studentId: String?
    let date: Date?
    
    var path: String { APIConstants.Endpoints.webcamSessions }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(studentId: String? = nil, date: Date? = nil) {
        self.studentId = studentId
        self.date = date
    }
}

// MARK: - Family Endpoints
struct GetFamiliesEndpoint: APIEndpoint {
    let page: Int
    let pageSize: Int
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.families }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(page: Int = 1, pageSize: Int = 20, filters: [String: Any]? = nil) {
        self.page = page
        self.pageSize = pageSize
        self.filters = filters
    }
}

// MARK: - Staff Endpoints
struct GetStaffEndpoint: APIEndpoint {
    let page: Int
    let pageSize: Int
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.staff }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(page: Int = 1, pageSize: Int = 20, filters: [String: Any]? = nil) {
        self.page = page
        self.pageSize = pageSize
        self.filters = filters
    }
}

// MARK: - Lessons Endpoints
struct GetLessonsEndpoint: APIEndpoint {
    let page: Int
    let pageSize: Int
    let filters: [String: Any]?
    
    var path: String { APIConstants.Endpoints.lessons }
    var method: HTTPMethod { .GET }
    var headers: [String: String] { [:] }
    var body: [String: Any]? { nil }
    var requiresAuth: Bool { true }
    
    init(page: Int = 1, pageSize: Int = 20, filters: [String: Any]? = nil) {
        self.page = page
        self.pageSize = pageSize
        self.filters = filters
    }
}

// MARK: - Auth Manager Protocol
protocol AuthManagerProtocol {
    var accessToken: String? { get }
    func refreshToken(completion: @escaping (Bool) -> Void)
}

// MARK: - Mock Auth Manager for Preview
class MockAuthManager: AuthManagerProtocol {
    var accessToken: String? = "mock_token"
    
    func refreshToken(completion: @escaping (Bool) -> Void) {
        completion(true)
    }
}