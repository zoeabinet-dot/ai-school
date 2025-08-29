import Foundation
import Combine

class RealAPIService: APIServiceProtocol {
    
    private let baseURL: String
    private let authToken: String?
    private let session: URLSession
    
    init(baseURL: String = "http://localhost:8000/", authToken: String? = nil) {
        self.baseURL = baseURL
        self.authToken = authToken
        
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: config)
    }
    
    // MARK: - Authentication
    
    func login(email: String, password: String, role: String) -> AnyPublisher<LoginResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/accounts/login/"
        let body = LoginRequest(email: email, password: password, role: role)
        
        return makeRequest(endpoint: endpoint, method: "POST", body: body)
    }
    
    func logout() -> AnyPublisher<EmptyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/accounts/logout/"
        return makeRequest(endpoint: endpoint, method: "POST")
    }
    
    func getProfile() -> AnyPublisher<UserResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/accounts/profile/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    // MARK: - Students
    
    func fetchStudents() -> AnyPublisher<StudentsResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/students/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func createStudent(_ student: Student) -> AnyPublisher<StudentResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/students/"
        return makeRequest(endpoint: endpoint, method: "POST", body: student)
    }
    
    func updateStudent(_ student: Student) -> AnyPublisher<StudentResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/students/\(student.id)/"
        return makeRequest(endpoint: endpoint, method: "PUT", body: student)
    }
    
    func deleteStudent(id: String) -> AnyPublisher<EmptyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/students/\(id)/"
        return makeRequest(endpoint: endpoint, method: "DELETE")
    }
    
    // MARK: - AI Lessons
    
    func fetchAILessons() -> AnyPublisher<AILessonsResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/ai-teacher/lessons/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func createAILesson(_ lesson: AILesson) -> AnyPublisher<AILessonResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/ai-teacher/lessons/"
        return makeRequest(endpoint: endpoint, method: "POST", body: lesson)
    }
    
    func updateAILesson(_ lesson: AILesson) -> AnyPublisher<AILessonResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/ai-teacher/lessons/\(lesson.id)/"
        return makeRequest(endpoint: endpoint, method: "PUT", body: lesson)
    }
    
    func deleteAILesson(id: String) -> AnyPublisher<EmptyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/ai-teacher/lessons/\(id)/"
        return makeRequest(endpoint: endpoint, method: "DELETE")
    }
    
    // MARK: - Analytics
    
    func fetchAnalytics() -> AnyPublisher<AnalyticsResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/analytics/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    // MARK: - Monitoring
    
    func fetchMonitoringData() -> AnyPublisher<MonitoringResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/monitoring/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func toggleMonitoring(isActive: Bool) -> AnyPublisher<MonitoringResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/monitoring/toggle/"
        let body = MonitoringToggleRequest(isActive: isActive)
        return makeRequest(endpoint: endpoint, method: "POST", body: body)
    }
    
    func updatePrivacySettings(settings: PrivacySettingsRequest) -> AnyPublisher<MonitoringResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/monitoring/privacy-settings/"
        return makeRequest(endpoint: endpoint, method: "POST", body: settings)
    }
    
    // MARK: - Families
    
    func fetchFamilyData() -> AnyPublisher<FamilyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/families/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func addFamilyMember(_ member: FamilyMember) -> AnyPublisher<FamilyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/families/members/"
        return makeRequest(endpoint: endpoint, method: "POST", body: member)
    }
    
    func removeFamilyMember(id: String) -> AnyPublisher<FamilyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/families/members/\(id)/"
        return makeRequest(endpoint: endpoint, method: "DELETE")
    }
    
    // MARK: - Staff
    
    func fetchStaffData() -> AnyPublisher<StaffResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/staff/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func createStaff(_ staff: Staff) -> AnyPublisher<StaffResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/staff/"
        return makeRequest(endpoint: endpoint, method: "POST", body: staff)
    }
    
    func updateStaff(_ staff: Staff) -> AnyPublisher<StaffResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/staff/\(staff.id)/"
        return makeRequest(endpoint: endpoint, method: "PUT", body: staff)
    }
    
    func deleteStaff(id: String) -> AnyPublisher<EmptyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/staff/\(id)/"
        return makeRequest(endpoint: endpoint, method: "DELETE")
    }
    
    // MARK: - Lessons
    
    func fetchLessons() -> AnyPublisher<LessonsResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/lessons/"
        return makeRequest(endpoint: endpoint, method: "GET")
    }
    
    func createLesson(_ lesson: Lesson) -> AnyPublisher<LessonResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/lessons/"
        return makeRequest(endpoint: endpoint, method: "POST", body: lesson)
    }
    
    func updateLesson(_ lesson: Lesson) -> AnyPublisher<LessonResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/lessons/\(lesson.id)/"
        return makeRequest(endpoint: endpoint, method: "PUT", body: lesson)
    }
    
    func deleteLesson(id: String) -> AnyPublisher<EmptyResponse, APIError> {
        let endpoint = "\(baseURL)api/v1/lessons/\(id)/"
        return makeRequest(endpoint: endpoint, method: "DELETE")
    }
    
    // MARK: - Private Methods
    
    private func makeRequest<T: Codable, U: Codable>(
        endpoint: String,
        method: String,
        body: T? = nil
    ) -> AnyPublisher<U, APIError> {
        
        guard let url = URL(string: endpoint) else {
            return Fail(error: APIError.invalidURL)
                .eraseToAnyPublisher()
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let authToken = authToken {
            request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        }
        
        if let body = body {
            do {
                request.httpBody = try JSONEncoder().encode(body)
            } catch {
                return Fail(error: APIError.encodingError)
                    .eraseToAnyPublisher()
            }
        }
        
        return session.dataTaskPublisher(for: request)
            .tryMap { data, response in
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw APIError.invalidResponse
                }
                
                if httpResponse.statusCode >= 400 {
                    throw APIError.httpError(httpResponse.statusCode)
                }
                
                return data
            }
            .decode(type: U.self, decoder: JSONDecoder())
            .mapError { error in
                if let apiError = error as? APIError {
                    return apiError
                }
                return APIError.decodingError
            }
            .eraseToAnyPublisher()
    }
}

// MARK: - API Configuration

struct APIConfig {
    static let baseURL = "http://localhost:8000/"
    static let productionBaseURL = "https://api.addisababa-aischool.com/"
    
    static func getBaseURL(isProduction: Bool = false) -> String {
        return isProduction ? productionBaseURL : baseURL
    }
}

// MARK: - API Error

enum APIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(Int)
    case encodingError
    case decodingError
    case networkError
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let code):
            return "HTTP error: \(code)"
        case .encodingError:
            return "Failed to encode request data"
        case .decodingError:
            return "Failed to decode response data"
        case .networkError:
            return "Network error occurred"
        }
    }
}