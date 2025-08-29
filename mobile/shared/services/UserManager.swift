import Foundation
import Combine

// MARK: - User Manager
class UserManager: ObservableObject {
    static let shared = UserManager()
    
    @Published var currentUser: User?
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let authManager: AuthManagerProtocol
    private let networkService: NetworkServiceProtocol
    private var cancellables = Set<AnyCancellable>()
    
    init(authManager: AuthManagerProtocol = MockAuthManager(), 
         networkService: NetworkServiceProtocol = NetworkService.shared) {
        self.authManager = authManager
        self.networkService = networkService
        checkAuthenticationStatus()
    }
    
    // MARK: - Authentication Methods
    
    func login(email: String, password: String, role: UserRole) async {
        await MainActor.run {
            isLoading = true
            errorMessage = nil
        }
        
        do {
            let endpoint = LoginEndpoint(email: email, password: password, role: role)
            let response: AuthResponse = try await withCheckedThrowingContinuation { continuation in
                networkService.request(endpoint)
                    .sink(
                        receiveCompletion: { completion in
                            switch completion {
                            case .finished:
                                break
                            case .failure(let error):
                                continuation.resume(throwing: error)
                            }
                        },
                        receiveValue: { response in
                            continuation.resume(returning: response)
                        }
                    )
                    .store(in: &cancellables)
            }
            
            await MainActor.run {
                self.currentUser = response.user
                self.isAuthenticated = true
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func logout() {
        Task {
            do {
                let endpoint = LogoutEndpoint()
                let _: EmptyResponse = try await withCheckedThrowingContinuation { continuation in
                    networkService.request(endpoint)
                        .sink(
                            receiveCompletion: { completion in
                                switch completion {
                                case .finished:
                                    break
                                case .failure(let error):
                                    continuation.resume(throwing: error)
                                }
                            },
                            receiveValue: { response in
                                continuation.resume(returning: response)
                            }
                        )
                        .store(in: &cancellables)
                }
                
                await MainActor.run {
                    self.currentUser = nil
                    self.isAuthenticated = false
                }
            } catch {
                await MainActor.run {
                    self.errorMessage = error.localizedDescription
                }
            }
        }
    }
    
    func refreshUserProfile() async {
        await MainActor.run {
            isLoading = true
        }
        
        do {
            let endpoint = GetUserProfileEndpoint()
            let user: User = try await withCheckedThrowingContinuation { continuation in
                networkService.request(endpoint)
                    .sink(
                        receiveCompletion: { completion in
                            switch completion {
                            case .finished:
                                break
                            case .failure(let error):
                                continuation.resume(throwing: error)
                            }
                        },
                        receiveValue: { user in
                            continuation.resume(returning: user)
                        }
                    )
                    .store(in: &cancellables)
            }
            
            await MainActor.run {
                self.currentUser = user
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    private func checkAuthenticationStatus() {
        isAuthenticated = authManager.accessToken != nil
        if isAuthenticated {
            Task {
                await refreshUserProfile()
            }
        }
    }
}

// MARK: - Response Models
struct AuthResponse: Codable {
    let user: User
    let accessToken: String
    let refreshToken: String
    let expiresIn: Int
    
    enum CodingKeys: String, CodingKey {
        case user
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case expiresIn = "expires_in"
    }
}

struct EmptyResponse: Codable {}

// MARK: - User Role
enum UserRole: String, Codable, CaseIterable {
    case student = "student"
    case family = "family"
    case staff = "staff"
    case admin = "admin"
    case aiTeacher = "ai_teacher"
    
    var displayName: String {
        switch self {
        case .student:
            return "Student"
        case .family:
            return "Family"
        case .staff:
            return "Staff"
        case .admin:
            return "Administrator"
        case .aiTeacher:
            return "AI Teacher"
        }
    }
}

// MARK: - Permission
enum Permission: String, Codable, CaseIterable {
    case viewOwnProfile = "view_own_profile"
    case editOwnProfile = "edit_own_profile"
    case viewOwnGrades = "view_own_grades"
    case viewOwnProgress = "view_own_progress"
    case participateInLessons = "participate_in_lessons"
    case viewStudents = "view_students"
    case editStudents = "edit_students"
    case viewStaff = "view_staff"
    case editStaff = "edit_staff"
    case viewAnalytics = "view_analytics"
    case viewMonitoring = "view_monitoring"
    case manageSystem = "manage_system"
    case aiLessonCreation = "ai_lesson_creation"
    case familyCommunication = "family_communication"
    
    var displayName: String {
        switch self {
        case .viewOwnProfile:
            return "View Own Profile"
        case .editOwnProfile:
            return "Edit Own Profile"
        case .viewOwnGrades:
            return "View Own Grades"
        case .viewOwnProgress:
            return "View Own Progress"
        case .participateInLessons:
            return "Participate in Lessons"
        case .viewStudents:
            return "View Students"
        case .editStudents:
            return "Edit Students"
        case .viewStaff:
            return "View Staff"
        case .editStaff:
            return "Edit Staff"
        case .viewAnalytics:
            return "View Analytics"
        case .viewMonitoring:
            return "View Monitoring"
        case .manageSystem:
            return "Manage System"
        case .aiLessonCreation:
            return "AI Lesson Creation"
        case .familyCommunication:
            return "Family Communication"
        }
    }
}