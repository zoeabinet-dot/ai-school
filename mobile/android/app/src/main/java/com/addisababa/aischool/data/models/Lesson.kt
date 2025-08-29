package com.addisababa.aischool.data.models

import java.util.UUID

data class Lesson(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val subject: String,
    val description: String,
    val teacher: String,
    val duration: String,
    val studentCount: Int,
    val status: LessonStatus,
    val date: String
)

enum class LessonStatus(val displayName: String) {
    ACTIVE("Active"),
    COMPLETED("Completed"),
    SCHEDULED("Scheduled")
}

// MARK: - Mock Data
object MockData {
    fun getMockLessons(): List<Lesson> {
        return listOf(
            Lesson(
                title = "Introduction to Algebra",
                subject = "Mathematics",
                description = "Basic algebraic concepts and problem-solving techniques",
                teacher = "Dr. Sarah Ahmed",
                duration = "45 min",
                studentCount = 25,
                status = LessonStatus.ACTIVE,
                date = "Today, 10:00 AM"
            ),
            Lesson(
                title = "Physics Lab: Motion",
                subject = "Physics",
                description = "Hands-on experiments with motion and forces",
                teacher = "Mr. Michael Tesfaye",
                duration = "60 min",
                studentCount = 20,
                status = LessonStatus.SCHEDULED,
                date = "Tomorrow, 2:00 PM"
            ),
            Lesson(
                title = "English Literature",
                subject = "English",
                description = "Analysis of classic literature and poetry",
                teacher = "Ms. Fatima Hassan",
                duration = "50 min",
                studentCount = 30,
                status = LessonStatus.COMPLETED,
                date = "Yesterday, 1:30 PM"
            ),
            Lesson(
                title = "Computer Programming",
                subject = "Computer Science",
                description = "Introduction to Python programming language",
                teacher = "Mr. David Bekele",
                duration = "75 min",
                studentCount = 18,
                status = LessonStatus.ACTIVE,
                date = "Today, 3:15 PM"
            ),
            Lesson(
                title = "History: Ancient Civilizations",
                subject = "History",
                description = "Exploration of ancient Egyptian and Greek civilizations",
                teacher = "Ms. Aisha Mohammed",
                duration = "40 min",
                studentCount = 28,
                status = LessonStatus.SCHEDULED,
                date = "Wednesday, 11:00 AM"
            ),
            Lesson(
                title = "Chemistry: Chemical Reactions",
                subject = "Chemistry",
                description = "Understanding chemical reactions and equations",
                teacher = "Dr. Sarah Ahmed",
                duration = "55 min",
                studentCount = 22,
                status = LessonStatus.COMPLETED,
                date = "Monday, 9:00 AM"
            )
        )
    }
}