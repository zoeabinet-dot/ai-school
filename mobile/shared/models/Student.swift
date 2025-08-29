import Foundation

// MARK: - Student Model
struct Student: Codable, Identifiable, Equatable {
    let id: UUID
    let firstName: String
    let lastName: String
    let email: String
    let phone: String
    let grade: String
    let age: Int
    let address: String
    let city: String
    let profileImage: String?
    let status: StudentStatus
    let averageScore: Int
    let enrollmentDate: Date
    let guardianName: String?
    let guardianPhone: String?
    let guardianEmail: String?
    let academicLevel: AcademicLevel
    let learningStyle: LearningStyle?
    let specialNeeds: [SpecialNeed]?
    let interests: [String]?
    let goals: [StudentGoal]?
    let achievements: [Achievement]?
    
    var fullName: String {
        "\(firstName) \(lastName)"
    }
    
    var displayName: String {
        fullName
    }
    
    var initials: String {
        let firstInitial = firstName.prefix(1).uppercased()
        let lastInitial = lastName.prefix(1).uppercased()
        return "\(firstInitial)\(lastInitial)"
    }
    
    enum CodingKeys: String, CodingKey {
        case id
        case firstName = "first_name"
        case lastName = "last_name"
        case email
        case phone
        case grade
        case age
        case address
        case city
        case profileImage = "profile_image"
        case status
        case averageScore = "average_score"
        case enrollmentDate = "enrollment_date"
        case guardianName = "guardian_name"
        case guardianPhone = "guardian_phone"
        case guardianEmail = "guardian_email"
        case academicLevel = "academic_level"
        case learningStyle = "learning_style"
        case specialNeeds = "special_needs"
        case interests
        case goals
        case achievements
    }
}

// MARK: - Student Status
enum StudentStatus: String, Codable, CaseIterable {
    case active = "active"
    case inactive = "inactive"
    case pending = "pending"
    case graduated = "graduated"
    case transferred = "transferred"
    
    var displayName: String {
        switch self {
        case .active:
            return "Active"
        case .inactive:
            return "Inactive"
        case .pending:
            return "Pending"
        case .graduated:
            return "Graduated"
        case .transferred:
            return "Transferred"
        }
    }
}

// MARK: - Academic Level
enum AcademicLevel: String, Codable, CaseIterable {
    case beginner = "beginner"
    case intermediate = "intermediate"
    case advanced = "advanced"
    case gifted = "gifted"
    
    var displayName: String {
        switch self {
        case .beginner:
            return "Beginner"
        case .intermediate:
            return "Intermediate"
        case .advanced:
            return "Advanced"
        case .gifted:
            return "Gifted"
        }
    }
}

// MARK: - Learning Style
enum LearningStyle: String, Codable, CaseIterable {
    case visual = "visual"
    case auditory = "auditory"
    case kinesthetic = "kinesthetic"
    case reading = "reading"
    case mixed = "mixed"
    
    var displayName: String {
        switch self {
        case .visual:
            return "Visual"
        case .auditory:
            return "Auditory"
        case .kinesthetic:
            return "Kinesthetic"
        case .reading:
            return "Reading/Writing"
        case .mixed:
            return "Mixed"
        }
    }
}

// MARK: - Special Need
struct SpecialNeed: Codable, Identifiable, Equatable {
    let id: UUID
    let name: String
    let description: String
    let accommodations: [String]
    let severity: SpecialNeedSeverity
    
    enum CodingKeys: String, CodingKey {
        case id
        case name
        case description
        case accommodations
        case severity
    }
}

// MARK: - Special Need Severity
enum SpecialNeedSeverity: String, Codable, CaseIterable {
    case mild = "mild"
    case moderate = "moderate"
    case severe = "severe"
    
    var displayName: String {
        switch self {
        case .mild:
            return "Mild"
        case .moderate:
            return "Moderate"
        case .severe:
            return "Severe"
        }
    }
}

// MARK: - Student Goal
struct StudentGoal: Codable, Identifiable, Equatable {
    let id: UUID
    let title: String
    let description: String
    let targetDate: Date
    let progress: Int
    let isCompleted: Bool
    let category: GoalCategory
    
    enum CodingKeys: String, CodingKey {
        case id
        case title
        case description
        case targetDate = "target_date"
        case progress
        case isCompleted = "is_completed"
        case category
    }
}

// MARK: - Goal Category
enum GoalCategory: String, Codable, CaseIterable {
    case academic = "academic"
    case personal = "personal"
    case social = "social"
    case career = "career"
    case health = "health"
    
    var displayName: String {
        switch self {
        case .academic:
            return "Academic"
        case .personal:
            return "Personal"
        case .social:
            return "Social"
        case .career:
            return "Career"
        case .health:
            return "Health"
        }
    }
}

// MARK: - Achievement
struct Achievement: Codable, Identifiable, Equatable {
    let id: UUID
    let title: String
    let description: String
    let dateEarned: Date
    let category: AchievementCategory
    let points: Int
    let badge: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case title
        case description
        case dateEarned = "date_earned"
        case category
        case points
        case badge
    }
}

// MARK: - Achievement Category
enum AchievementCategory: String, Codable, CaseIterable {
    case academic = "academic"
    case leadership = "leadership"
    case creativity = "creativity"
    case sports = "sports"
    case community = "community"
    case innovation = "innovation"
    
    var displayName: String {
        switch self {
        case .academic:
            return "Academic"
        case .leadership:
            return "Leadership"
        case .creativity:
            return "Creativity"
        case .sports:
            return "Sports"
        case .community:
            return "Community"
        case .innovation:
            return "Innovation"
        }
    }
}

// MARK: - Student Extensions
extension Student {
    static func mock() -> Student {
        Student(
            id: UUID(),
            firstName: "Abebe",
            lastName: "Kebede",
            email: "abebe.kebede@addisababa-aischool.com",
            phone: "+251911234567",
            grade: "Grade 8",
            age: 14,
            address: "123 Bole Road",
            city: "Addis Ababa",
            profileImage: nil,
            status: .active,
            averageScore: 85,
            enrollmentDate: Date(),
            guardianName: "Kebede Alemu",
            guardianPhone: "+251922345678",
            guardianEmail: "kebede.alemu@email.com",
            academicLevel: .intermediate,
            learningStyle: .visual,
            specialNeeds: [],
            interests: ["Mathematics", "Science", "Technology"],
            goals: [
                StudentGoal(
                    id: UUID(),
                    title: "Improve Math Skills",
                    description: "Achieve 90% in mathematics by end of semester",
                    targetDate: Date().addingTimeInterval(86400 * 90),
                    progress: 75,
                    isCompleted: false,
                    category: .academic
                )
            ],
            achievements: [
                Achievement(
                    id: UUID(),
                    title: "Perfect Attendance",
                    description: "Attended all classes for 3 months",
                    dateEarned: Date().addingTimeInterval(-86400 * 30),
                    category: .academic,
                    points: 100,
                    badge: "attendance_badge"
                )
            ]
        )
    }
}

// MARK: - Mock Data
extension Student {
    static func mockStudents() -> [Student] {
        [
            Student.mock(),
            Student(
                id: UUID(),
                firstName: "Fatima",
                lastName: "Ahmed",
                email: "fatima.ahmed@addisababa-aischool.com",
                phone: "+251933456789",
                grade: "Grade 9",
                age: 15,
                address: "456 Kazanchis Street",
                city: "Addis Ababa",
                profileImage: nil,
                status: .active,
                averageScore: 92,
                enrollmentDate: Date(),
                guardianName: "Ahmed Hassan",
                guardianPhone: "+251944567890",
                guardianEmail: "ahmed.hassan@email.com",
                academicLevel: .advanced,
                learningStyle: .auditory,
                specialNeeds: [],
                interests: ["Literature", "History", "Languages"],
                goals: [],
                achievements: []
            ),
            Student(
                id: UUID(),
                firstName: "Yohannes",
                lastName: "Tadesse",
                email: "yohannes.tadesse@addisababa-aischool.com",
                phone: "+251955678901",
                grade: "Grade 7",
                age: 13,
                address: "789 Piazza Street",
                city: "Addis Ababa",
                profileImage: nil,
                status: .active,
                averageScore: 78,
                enrollmentDate: Date(),
                guardianName: "Tadesse Bekele",
                guardianPhone: "+251966789012",
                guardianEmail: "tadesse.bekele@email.com",
                academicLevel: .beginner,
                learningStyle: .kinesthetic,
                specialNeeds: [],
                interests: ["Sports", "Art", "Music"],
                goals: [],
                achievements: []
            )
        ]
    }
}