package com.addisababa.aischool.data.models

import java.util.UUID

data class StaffData(
    val staff: List<Staff>,
    val assignments: List<StaffAssignment>,
    val performance: StaffPerformance
)

data class Staff(
    val id: UUID = UUID.randomUUID(),
    val fullName: String,
    val initials: String,
    val role: StaffRole,
    val isActive: Boolean
)

data class StaffAssignment(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val staffName: String,
    val status: AssignmentStatus,
    val dueDate: String
)

data class StaffPerformance(
    val averageRating: Double,
    val tasksCompleted: Int,
    val studentsCount: Int
)

enum class StaffRole(val displayName: String) {
    TEACHER("Teacher"),
    ADMINISTRATOR("Administrator"),
    COUNSELOR("Counselor"),
    SUPPORT_STAFF("Support Staff"),
    IT_STAFF("IT Staff")
}

enum class AssignmentStatus(val displayName: String) {
    ACTIVE("Active"),
    COMPLETED("Completed"),
    PENDING("Pending")
}

// MARK: - Mock Data
object MockData {
    fun getMockStaffData(): StaffData {
        return StaffData(
            staff = listOf(
                Staff(
                    fullName = "Dr. Sarah Ahmed",
                    initials = "SA",
                    role = StaffRole.TEACHER,
                    isActive = true
                ),
                Staff(
                    fullName = "Mr. Michael Tesfaye",
                    initials = "MT",
                    role = StaffRole.TEACHER,
                    isActive = true
                ),
                Staff(
                    fullName = "Ms. Fatima Hassan",
                    initials = "FH",
                    role = StaffRole.ADMINISTRATOR,
                    isActive = true
                ),
                Staff(
                    fullName = "Mr. David Bekele",
                    initials = "DB",
                    role = StaffRole.COUNSELOR,
                    isActive = true
                ),
                Staff(
                    fullName = "Ms. Aisha Mohammed",
                    initials = "AM",
                    role = StaffRole.SUPPORT_STAFF,
                    isActive = false
                )
            ),
            assignments = listOf(
                StaffAssignment(
                    title = "Grade 10 Mathematics",
                    staffName = "Dr. Sarah Ahmed",
                    status = AssignmentStatus.ACTIVE,
                    dueDate = "Ongoing"
                ),
                StaffAssignment(
                    title = "Student Counseling Session",
                    staffName = "Mr. David Bekele",
                    status = AssignmentStatus.PENDING,
                    dueDate = "Tomorrow"
                ),
                StaffAssignment(
                    title = "Administrative Review",
                    staffName = "Ms. Fatima Hassan",
                    status = AssignmentStatus.COMPLETED,
                    dueDate = "Completed"
                ),
                StaffAssignment(
                    title = "Science Lab Setup",
                    staffName = "Mr. Michael Tesfaye",
                    status = AssignmentStatus.ACTIVE,
                    dueDate = "This Week"
                )
            ),
            performance = StaffPerformance(
                averageRating = 4.5,
                tasksCompleted = 156,
                studentsCount = 245
            )
        )
    }
}