import Foundation

// MARK: - API Configuration
struct APIConstants {
    static let baseURL = "https://api.addisababa-aischool.com"
    static let apiVersion = "v1"
    static let timeoutInterval: TimeInterval = 30.0
    
    // Endpoints
    struct Endpoints {
        // Authentication
        static let login = "/auth/login/"
        static let logout = "/auth/logout/"
        static let refreshToken = "/auth/refresh/"
        static let register = "/auth/register/"
        
        // Users
        static let users = "/users/"
        static let profile = "/users/profile/"
        static let changePassword = "/users/change-password/"
        
        // Students
        static let students = "/students/"
        static let studentProfile = "/students/{id}/"
        static let academicRecords = "/students/{id}/academic-records/"
        static let projects = "/students/{id}/projects/"
        static let learningSessions = "/students/{id}/learning-sessions/"
        static let goals = "/students/{id}/goals/"
        static let dashboard = "/students/{id}/dashboard/"
        
        // AI Teacher
        static let aiLessons = "/ai-teacher/lessons/"
        static let aiLessonDetail = "/ai-teacher/lessons/{id}/"
        static let aiSessions = "/ai-teacher/sessions/"
        static let aiProgress = "/ai-teacher/progress/"
        static let aiRecommendations = "/ai-teacher/recommendations/"
        
        // Analytics
        static let learningAnalytics = "/analytics/learning/"
        static let performanceMetrics = "/analytics/performance/"
        static let engagementAnalytics = "/analytics/engagement/"
        static let studentAnalytics = "/analytics/students/{id}/"
        static let classAnalytics = "/analytics/classes/{id}/"
        
        // Monitoring
        static let webcamSessions = "/monitoring/webcam-sessions/"
        static let frameAnalysis = "/monitoring/frame-analysis/"
        static let behaviorEvents = "/monitoring/behavior-events/"
        static let privacySettings = "/monitoring/privacy-settings/"
        static let monitoringAlerts = "/monitoring/alerts/"
        
        // Families
        static let families = "/families/"
        static let familyMembers = "/families/{id}/members/"
        static let familyStudents = "/families/{id}/students/"
        static let familyDashboard = "/families/{id}/dashboard/"
        
        // Staff
        static let staff = "/staff/"
        static let staffProfile = "/staff/{id}/"
        static let staffAssignments = "/staff/{id}/assignments/"
        static let staffDashboard = "/staff/{id}/dashboard/"
        
        // Lessons
        static let lessons = "/lessons/"
        static let lessonPlans = "/lessons/{id}/plans/"
        static let lessonMaterials = "/lessons/{id}/materials/"
        static let lessonAssessments = "/lessons/{id}/assessments/"
    }
}

// MARK: - User Roles
enum UserRole: String, CaseIterable, Codable {
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
    
    var permissions: [Permission] {
        switch self {
        case .student:
            return [.viewOwnProfile, .viewOwnGrades, .participateInLessons, .viewOwnProgress]
        case .family:
            return [.viewFamilyProfile, .viewChildrenProgress, .communicateWithStaff, .viewFamilyDashboard]
        case .staff:
            return [.viewStudents, .manageLessons, .viewAnalytics, .viewStaffDashboard]
        case .admin:
            return Permission.allCases
        case .aiTeacher:
            return [.createLessons, .analyzeProgress, .generateRecommendations, .monitorStudents]
        }
    }
}

// MARK: - Permissions
enum Permission: String, CaseIterable, Codable {
    case viewOwnProfile = "view_own_profile"
    case viewOwnGrades = "view_own_grades"
    case participateInLessons = "participate_in_lessons"
    case viewOwnProgress = "view_own_progress"
    case viewFamilyProfile = "view_family_profile"
    case viewChildrenProgress = "view_children_progress"
    case communicateWithStaff = "communicate_with_staff"
    case viewFamilyDashboard = "view_family_dashboard"
    case viewStudents = "view_students"
    case manageLessons = "manage_lessons"
    case viewAnalytics = "view_analytics"
    case viewStaffDashboard = "view_staff_dashboard"
    case createLessons = "create_lessons"
    case analyzeProgress = "analyze_progress"
    case generateRecommendations = "generate_recommendations"
    case monitorStudents = "monitor_students"
    case manageUsers = "manage_users"
    case manageSystem = "manage_system"
}

// MARK: - Time Ranges
enum TimeRange: String, CaseIterable, Codable {
    case day = "day"
    case week = "week"
    case month = "month"
    case quarter = "quarter"
    case year = "year"
    
    var displayName: String {
        switch self {
        case .day:
            return "Today"
        case .week:
            return "This Week"
        case .month:
            return "This Month"
        case .quarter:
            return "This Quarter"
        case .year:
            return "This Year"
        }
    }
    
    var days: Int {
        switch self {
        case .day:
            return 1
        case .week:
            return 7
        case .month:
            return 30
        case .quarter:
            return 90
        case .year:
            return 365
        }
    }
}

// MARK: - Academic Constants
struct AcademicConstants {
    static let gradeScale = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
    static let passingGrade = "D-"
    static let maxGradePoints = 4.0
    
    static let subjectCategories = [
        "Mathematics",
        "Science",
        "Language Arts",
        "Social Studies",
        "Physical Education",
        "Arts & Music",
        "Technology",
        "Foreign Languages"
    ]
    
    static let assessmentTypes = [
        "Quiz",
        "Test",
        "Exam",
        "Project",
        "Presentation",
        "Participation",
        "Homework",
        "Lab Work"
    ]
}

// MARK: - AI Constants
struct AIConstants {
    static let maxLessonDuration: TimeInterval = 3600 // 1 hour
    static let minLessonDuration: TimeInterval = 900 // 15 minutes
    
    static let supportedLanguages = [
        "English",
        "Amharic",
        "Oromo",
        "Tigrinya",
        "Somali",
        "French",
        "Arabic"
    ]
    
    static let aiModelTypes = [
        "GPT-4",
        "GPT-3.5",
        "Claude",
        "Gemini",
        "Custom"
    ]
    
    static let speechRecognitionLanguages = [
        "en-US",
        "am-ET",
        "om-ET",
        "ti-ET",
        "so-ET"
    ]
}

// MARK: - Monitoring Constants
struct MonitoringConstants {
    static let maxRecordingDuration: TimeInterval = 28800 // 8 hours
    static let frameAnalysisInterval: TimeInterval = 1.0 // 1 second
    static let privacyBlurRadius: CGFloat = 20.0
    
    static let behaviorCategories = [
        "Engagement",
        "Attention",
        "Participation",
        "Collaboration",
        "Disruption",
        "Safety"
    ]
    
    static let alertLevels = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]
}

// MARK: - UI Constants
struct UIConstants {
    static let cornerRadius: CGFloat = 12.0
    static let shadowRadius: CGFloat = 5.0
    static let shadowOpacity: Float = 0.1
    
    static let animationDuration: Double = 0.3
    static let longAnimationDuration: Double = 0.6
    
    static let spacing: CGFloat = 16.0
    static let smallSpacing: CGFloat = 8.0
    static let largeSpacing: CGFloat = 24.0
    
    static let buttonHeight: CGFloat = 50.0
    static let inputFieldHeight: CGFloat = 44.0
}

// MARK: - Storage Keys
struct StorageKeys {
    static let authToken = "auth_token"
    static let refreshToken = "refresh_token"
    static let userProfile = "user_profile"
    static let appSettings = "app_settings"
    static let offlineData = "offline_data"
    static let biometricEnabled = "biometric_enabled"
    static let lastSync = "last_sync"
}

// MARK: - Error Messages
struct ErrorMessages {
    static let networkError = "Network connection error. Please check your internet connection."
    static let authenticationError = "Authentication failed. Please log in again."
    static let serverError = "Server error. Please try again later."
    static let unknownError = "An unknown error occurred. Please try again."
    static let permissionDenied = "Permission denied. Please contact your administrator."
    static let dataNotFound = "Requested data not found."
    static let validationError = "Please check your input and try again."
}