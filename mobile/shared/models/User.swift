import Foundation

// MARK: - User Model
struct User: Codable, Identifiable, Equatable {
    let id: String
    let email: String
    let firstName: String
    let lastName: String
    let role: UserRole
    let isActive: Bool
    let dateJoined: Date
    let lastLogin: Date?
    let profileImage: String?
    let phoneNumber: String?
    let dateOfBirth: Date?
    let gender: Gender?
    let address: Address?
    let preferences: UserPreferences
    let permissions: [Permission]
    let metadata: [String: String]
    
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
    
    var isOnline: Bool {
        // Calculate if user is online based on last activity
        guard let lastLogin = lastLogin else { return false }
        let timeSinceLastLogin = Date().timeIntervalSince(lastLogin)
        return timeSinceLastLogin < 300 // 5 minutes
    }
    
    enum CodingKeys: String, CodingKey {
        case id
        case email
        case firstName = "first_name"
        case lastName = "last_name"
        case role
        case isActive = "is_active"
        case dateJoined = "date_joined"
        case lastLogin = "last_login"
        case profileImage = "profile_image"
        case phoneNumber = "phone_number"
        case dateOfBirth = "date_of_birth"
        case gender
        case address
        case preferences
        case permissions
        case metadata
    }
}

// MARK: - Gender Enum
enum Gender: String, Codable, CaseIterable {
    case male = "male"
    case female = "female"
    case other = "other"
    case preferNotToSay = "prefer_not_to_say"
    
    var displayName: String {
        switch self {
        case .male:
            return "Male"
        case .female:
            return "Female"
        case .other:
            return "Other"
        case .preferNotToSay:
            return "Prefer not to say"
        }
    }
}

// MARK: - Address Model
struct Address: Codable, Equatable {
    let street: String
    let city: String
    let state: String
    let country: String
    let postalCode: String
    let coordinates: Coordinates?
    
    enum CodingKeys: String, CodingKey {
        case street
        case city
        case state
        case country
        case postalCode = "postal_code"
        case coordinates
    }
    
    var formattedAddress: String {
        "\(street), \(city), \(state) \(postalCode), \(country)"
    }
}

// MARK: - Coordinates Model
struct Coordinates: Codable, Equatable {
    let latitude: Double
    let longitude: Double
    
    var coordinateString: String {
        "\(latitude), \(longitude)"
    }
}

// MARK: - User Preferences
struct UserPreferences: Codable, Equatable {
    let language: String
    let timezone: String
    let notifications: NotificationPreferences
    let privacy: PrivacyPreferences
    let accessibility: AccessibilityPreferences
    let theme: ThemePreference
    
    enum CodingKeys: String, CodingKey {
        case language
        case timezone
        case notifications
        case privacy
        case accessibility
        case theme
    }
}

// MARK: - Notification Preferences
struct NotificationPreferences: Codable, Equatable {
    let pushEnabled: Bool
    let emailEnabled: Bool
    let smsEnabled: Bool
    let academicUpdates: Bool
    let aiLessonUpdates: Bool
    let monitoringAlerts: Bool
    let familyCommunication: Bool
    let systemUpdates: Bool
    
    enum CodingKeys: String, CodingKey {
        case pushEnabled = "push_enabled"
        case emailEnabled = "email_enabled"
        case smsEnabled = "sms_enabled"
        case academicUpdates = "academic_updates"
        case aiLessonUpdates = "ai_lesson_updates"
        case monitoringAlerts = "monitoring_alerts"
        case familyCommunication = "family_communication"
        case systemUpdates = "system_updates"
    }
}

// MARK: - Privacy Preferences
struct PrivacyPreferences: Codable, Equatable {
    let profileVisibility: ProfileVisibility
    let academicRecordVisibility: AcademicRecordVisibility
    let monitoringConsent: Bool
    let dataSharing: DataSharingPreferences
    let locationSharing: Bool
    
    enum CodingKeys: String, CodingKey {
        case profileVisibility = "profile_visibility"
        case academicRecordVisibility = "academic_record_visibility"
        case monitoringConsent = "monitoring_consent"
        case dataSharing = "data_sharing"
        case locationSharing = "location_sharing"
    }
}

// MARK: - Profile Visibility
enum ProfileVisibility: String, Codable, CaseIterable {
    case public = "public"
    case staffOnly = "staff_only"
    case familyOnly = "family_only"
    case private = "private"
    
    var displayName: String {
        switch self {
        case .public:
            return "Public"
        case .staffOnly:
            return "Staff Only"
        case .familyOnly:
            return "Family Only"
        case .private:
            return "Private"
        }
    }
}

// MARK: - Academic Record Visibility
enum AcademicRecordVisibility: String, Codable, CaseIterable {
    case public = "public"
    case staffOnly = "staff_only"
    case familyOnly = "family_only"
    case selfOnly = "self_only"
    
    var displayName: String {
        switch self {
        case .public:
            return "Public"
        case .staffOnly:
            return "Staff Only"
        case .familyOnly:
            return "Family Only"
        case .selfOnly:
            return "Self Only"
        }
    }
}

// MARK: - Data Sharing Preferences
struct DataSharingPreferences: Codable, Equatable {
    let analytics: Bool
    let research: Bool
    let thirdParty: Bool
    let aiTraining: Bool
    
    enum CodingKeys: String, CodingKey {
        case analytics
        case research
        case thirdParty = "third_party"
        case aiTraining = "ai_training"
    }
}

// MARK: - Accessibility Preferences
struct AccessibilityPreferences: Codable, Equatable {
    let highContrast: Bool
    let largeText: Bool
    let screenReader: Bool
    let reducedMotion: Bool
    let colorBlindness: ColorBlindnessType?
    
    enum CodingKeys: String, CodingKey {
        case highContrast = "high_contrast"
        case largeText = "large_text"
        case screenReader = "screen_reader"
        case reducedMotion = "reduced_motion"
        case colorBlindness = "color_blindness"
    }
}

// MARK: - Color Blindness Type
enum ColorBlindnessType: String, Codable, CaseIterable {
    case protanopia = "protanopia"
    case deuteranopia = "deuteranopia"
    case tritanopia = "tritanopia"
    case achromatopsia = "achromatopsia"
    
    var displayName: String {
        switch self {
        case .protanopia:
            return "Protanopia (Red-Blind)"
        case .deuteranopia:
            return "Deuteranopia (Green-Blind)"
        case .tritanopia:
            return "Tritanopia (Blue-Blind)"
        case .achromatopsia:
            return "Achromatopsia (Complete Color Blindness)"
        }
    }
}

// MARK: - Theme Preference
enum ThemePreference: String, Codable, CaseIterable {
    case light = "light"
    case dark = "dark"
    case system = "system"
    
    var displayName: String {
        switch self {
        case .light:
            return "Light"
        case .dark:
            return "Dark"
        case .system:
            return "System"
        }
    }
}

// MARK: - User Extensions
extension User {
    static func mock() -> User {
        User(
            id: "user_001",
            email: "john.doe@addisababa-aischool.com",
            firstName: "John",
            lastName: "Doe",
            role: .student,
            isActive: true,
            dateJoined: Date(),
            lastLogin: Date(),
            profileImage: nil,
            phoneNumber: "+251911234567",
            dateOfBirth: Calendar.current.date(from: DateComponents(year: 2008, month: 6, day: 15)),
            gender: .male,
            address: Address(
                street: "123 Bole Road",
                city: "Addis Ababa",
                state: "Addis Ababa",
                country: "Ethiopia",
                postalCode: "1000",
                coordinates: Coordinates(latitude: 9.0320, longitude: 38.7636)
            ),
            preferences: UserPreferences.mock(),
            permissions: [.viewOwnProfile, .viewOwnGrades, .participateInLessons, .viewOwnProgress],
            metadata: [:]
        )
    }
}

extension UserPreferences {
    static func mock() -> UserPreferences {
        UserPreferences(
            language: "en",
            timezone: "Africa/Addis_Ababa",
            notifications: NotificationPreferences.mock(),
            privacy: PrivacyPreferences.mock(),
            accessibility: AccessibilityPreferences.mock(),
            theme: .system
        )
    }
}

extension NotificationPreferences {
    static func mock() -> NotificationPreferences {
        NotificationPreferences(
            pushEnabled: true,
            emailEnabled: true,
            smsEnabled: false,
            academicUpdates: true,
            aiLessonUpdates: true,
            monitoringAlerts: false,
            familyCommunication: true,
            systemUpdates: false
        )
    }
}

extension PrivacyPreferences {
    static func mock() -> PrivacyPreferences {
        PrivacyPreferences(
            profileVisibility: .staffOnly,
            academicRecordVisibility: .familyOnly,
            monitoringConsent: true,
            dataSharing: DataSharingPreferences.mock(),
            locationSharing: false
        )
    }
}

extension DataSharingPreferences {
    static func mock() -> DataSharingPreferences {
        DataSharingPreferences(
            analytics: true,
            research: false,
            thirdParty: false,
            aiTraining: true
        )
    }
}

extension AccessibilityPreferences {
    static func mock() -> AccessibilityPreferences {
        AccessibilityPreferences(
            highContrast: false,
            largeText: false,
            screenReader: false,
            reducedMotion: false,
            colorBlindness: nil
        )
    }
}