package com.addisababa.aischool.data.models

import androidx.compose.ui.graphics.Color
import java.util.UUID

data class FamilyData(
    val family: Family,
    val members: List<FamilyMember>,
    val students: List<Student>,
    val communications: List<FamilyCommunication>
)

data class Family(
    val id: UUID = UUID.randomUUID(),
    val name: String,
    val memberCount: Int,
    val studentCount: Int,
    val activeMembers: Int
)

data class FamilyMember(
    val id: UUID = UUID.randomUUID(),
    val fullName: String,
    val initials: String,
    val relationship: FamilyRelationship,
    val isActive: Boolean
) {
    val fullName: String get() = fullName
}

data class FamilyCommunication(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val description: String,
    val type: CommunicationType,
    val date: String
)

enum class FamilyRelationship(val displayName: String) {
    PARENT("Parent"),
    GUARDIAN("Guardian"),
    SIBLING("Sibling"),
    GRANDPARENT("Grandparent"),
    OTHER("Other")
}

enum class CommunicationType(val icon: String, val color: Color) {
    EMAIL("📧", Color(0xFF2196F3)),
    SMS("💬", Color(0xFF4CAF50)),
    CALL("📞", Color(0xFFFF9800)),
    MEETING("🤝", Color(0xFF9C27B0)),
    NOTIFICATION("🔔", Color(0xFF607D8B))
}

// MARK: - Mock Data
object MockData {
    fun getMockFamilyData(): FamilyData {
        return FamilyData(
            family = Family(
                name = "Johnson Family",
                memberCount = 4,
                studentCount = 2,
                activeMembers = 3
            ),
            members = listOf(
                FamilyMember(
                    fullName = "Sarah Johnson",
                    initials = "SJ",
                    relationship = FamilyRelationship.PARENT,
                    isActive = true
                ),
                FamilyMember(
                    fullName = "Michael Johnson",
                    initials = "MJ",
                    relationship = FamilyRelationship.PARENT,
                    isActive = true
                ),
                FamilyMember(
                    fullName = "Emma Johnson",
                    initials = "EJ",
                    relationship = FamilyRelationship.SIBLING,
                    isActive = true
                ),
                FamilyMember(
                    fullName = "Robert Johnson",
                    initials = "RJ",
                    relationship = FamilyRelationship.GRANDPARENT,
                    isActive = false
                )
            ),
            students = listOf(
                Student(
                    id = UUID.randomUUID(),
                    firstName = "Alex",
                    lastName = "Johnson",
                    email = "alex.johnson@email.com",
                    phone = "+1234567890",
                    grade = "10",
                    age = 16,
                    address = "123 Main St",
                    city = "Addis Ababa",
                    profileImage = null,
                    status = StudentStatus.ACTIVE,
                    averageScore = 88,
                    enrollmentDate = "2023-09-01",
                    academicLevel = AcademicLevel.ADVANCED,
                    learningStyle = LearningStyle.VISUAL,
                    specialNeeds = emptyList(),
                    goals = emptyList(),
                    achievements = emptyList(),
                    emergencyContact = "Sarah Johnson",
                    emergencyPhone = "+1234567890",
                    medicalInfo = "No known allergies",
                    notes = "Excellent student with strong leadership skills"
                ),
                Student(
                    id = UUID.randomUUID(),
                    firstName = "Maya",
                    lastName = "Johnson",
                    email = "maya.johnson@email.com",
                    phone = "+1234567891",
                    grade = "8",
                    age = 14,
                    address = "123 Main St",
                    city = "Addis Ababa",
                    profileImage = null,
                    status = StudentStatus.ACTIVE,
                    averageScore = 92,
                    enrollmentDate = "2023-09-01",
                    academicLevel = AcademicLevel.ADVANCED,
                    learningStyle = LearningStyle.KINESTHETIC,
                    specialNeeds = emptyList(),
                    goals = emptyList(),
                    achievements = emptyList(),
                    emergencyContact = "Sarah Johnson",
                    emergencyPhone = "+1234567890",
                    medicalInfo = "No known allergies",
                    notes = "Creative student with strong artistic abilities"
                )
            ),
            communications = listOf(
                FamilyCommunication(
                    title = "Progress Report",
                    description = "Monthly progress report for Alex Johnson",
                    type = CommunicationType.EMAIL,
                    date = "Today, 3:45 PM"
                ),
                FamilyCommunication(
                    title = "Parent-Teacher Meeting",
                    description = "Scheduled meeting to discuss Maya's performance",
                    type = CommunicationType.MEETING,
                    date = "Yesterday, 2:30 PM"
                ),
                FamilyCommunication(
                    title = "Attendance Alert",
                    description = "Alex was absent from Mathematics class",
                    type = CommunicationType.NOTIFICATION,
                    date = "2 days ago"
                ),
                FamilyCommunication(
                    title = "Achievement Notification",
                    description = "Maya received an award for academic excellence",
                    type = CommunicationType.SMS,
                    date = "1 week ago"
                )
            )
        )
    }
}