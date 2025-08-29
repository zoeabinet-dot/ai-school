package com.addisababa.aischool.data.models

import java.util.UUID

data class Student(
    val id: UUID,
    val firstName: String,
    val lastName: String,
    val email: String,
    val phone: String,
    val grade: String,
    val age: Int,
    val address: String,
    val city: String,
    val profileImage: String?,
    val status: StudentStatus,
    val averageScore: Int,
    val enrollmentDate: String,
    val guardianName: String?,
    val guardianPhone: String?,
    val guardianEmail: String?,
    val academicLevel: AcademicLevel,
    val learningStyle: LearningStyle?,
    val specialNeeds: List<SpecialNeed>?,
    val interests: List<String>?,
    val goals: List<StudentGoal>?,
    val achievements: List<Achievement>?
) {
    val fullName: String
        get() = "$firstName $lastName"
    
    val displayName: String
        get() = fullName
    
    val initials: String
        get() = "${firstName.first().uppercase()}${lastName.first().uppercase()}"
}

enum class StudentStatus(val displayName: String) {
    ACTIVE("Active"),
    INACTIVE("Inactive"),
    PENDING("Pending"),
    GRADUATED("Graduated"),
    TRANSFERRED("Transferred")
}

enum class AcademicLevel(val displayName: String) {
    BEGINNER("Beginner"),
    INTERMEDIATE("Intermediate"),
    ADVANCED("Advanced"),
    GIFTED("Gifted")
}

enum class LearningStyle(val displayName: String) {
    VISUAL("Visual"),
    AUDITORY("Auditory"),
    KINESTHETIC("Kinesthetic"),
    READING("Reading/Writing"),
    MIXED("Mixed")
}

data class SpecialNeed(
    val id: UUID,
    val name: String,
    val description: String,
    val accommodations: List<String>,
    val severity: SpecialNeedSeverity
)

enum class SpecialNeedSeverity(val displayName: String) {
    MILD("Mild"),
    MODERATE("Moderate"),
    SEVERE("Severe")
}

data class StudentGoal(
    val id: UUID,
    val title: String,
    val description: String,
    val targetDate: String,
    val progress: Int,
    val isCompleted: Boolean,
    val category: GoalCategory
)

enum class GoalCategory(val displayName: String) {
    ACADEMIC("Academic"),
    PERSONAL("Personal"),
    SOCIAL("Social"),
    CAREER("Career"),
    HEALTH("Health")
}

data class Achievement(
    val id: UUID,
    val title: String,
    val description: String,
    val dateEarned: String,
    val category: AchievementCategory,
    val points: Int,
    val badge: String?
)

enum class AchievementCategory(val displayName: String) {
    ACADEMIC("Academic"),
    LEADERSHIP("Leadership"),
    CREATIVITY("Creativity"),
    SPORTS("Sports"),
    COMMUNITY("Community"),
    INNOVATION("Innovation")
}

// MARK: - Mock Data
object MockData {
    fun getMockStudents(): List<Student> {
        return listOf(
            Student(
                id = UUID.randomUUID(),
                firstName = "Abebe",
                lastName = "Kebede",
                email = "abebe.kebede@addisababa-aischool.com",
                phone = "+251911234567",
                grade = "Grade 8",
                age = 14,
                address = "123 Bole Road",
                city = "Addis Ababa",
                profileImage = null,
                status = StudentStatus.ACTIVE,
                averageScore = 85,
                enrollmentDate = "2024-01-15",
                guardianName = "Kebede Alemu",
                guardianPhone = "+251922345678",
                guardianEmail = "kebede.alemu@email.com",
                academicLevel = AcademicLevel.INTERMEDIATE,
                learningStyle = LearningStyle.VISUAL,
                specialNeeds = emptyList(),
                interests = listOf("Mathematics", "Science", "Technology"),
                goals = listOf(
                    StudentGoal(
                        id = UUID.randomUUID(),
                        title = "Improve Math Skills",
                        description = "Achieve 90% in mathematics by end of semester",
                        targetDate = "2024-06-15",
                        progress = 75,
                        isCompleted = false,
                        category = GoalCategory.ACADEMIC
                    )
                ),
                achievements = listOf(
                    Achievement(
                        id = UUID.randomUUID(),
                        title = "Perfect Attendance",
                        description = "Attended all classes for 3 months",
                        dateEarned = "2024-03-15",
                        category = AchievementCategory.ACADEMIC,
                        points = 100,
                        badge = "attendance_badge"
                    )
                )
            ),
            Student(
                id = UUID.randomUUID(),
                firstName = "Fatima",
                lastName = "Ahmed",
                email = "fatima.ahmed@addisababa-aischool.com",
                phone = "+251933456789",
                grade = "Grade 9",
                age = 15,
                address = "456 Kazanchis Street",
                city = "Addis Ababa",
                profileImage = null,
                status = StudentStatus.ACTIVE,
                averageScore = 92,
                enrollmentDate = "2024-01-10",
                guardianName = "Ahmed Hassan",
                guardianPhone = "+251944567890",
                guardianEmail = "ahmed.hassan@email.com",
                academicLevel = AcademicLevel.ADVANCED,
                learningStyle = LearningStyle.AUDITORY,
                specialNeeds = emptyList(),
                interests = listOf("Literature", "History", "Languages"),
                goals = emptyList(),
                achievements = emptyList()
            ),
            Student(
                id = UUID.randomUUID(),
                firstName = "Yohannes",
                lastName = "Tadesse",
                email = "yohannes.tadesse@addisababa-aischool.com",
                phone = "+251955678901",
                grade = "Grade 7",
                age = 13,
                address = "789 Piazza Street",
                city = "Addis Ababa",
                profileImage = null,
                status = StudentStatus.ACTIVE,
                averageScore = 78,
                enrollmentDate = "2024-01-20",
                guardianName = "Tadesse Bekele",
                guardianPhone = "+251966789012",
                guardianEmail = "tadesse.bekele@email.com",
                academicLevel = AcademicLevel.BEGINNER,
                learningStyle = LearningStyle.KINESTHETIC,
                specialNeeds = emptyList(),
                interests = listOf("Sports", "Art", "Music"),
                goals = emptyList(),
                achievements = emptyList()
            )
        )
    }
}