package com.addisababa.aischool.data.models

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import java.util.UUID

data class AnalyticsData(
    val averageScore: Int,
    val completionRate: Int,
    val studyTime: Int,
    val aiSessions: Int,
    val subjectPerformance: List<SubjectPerformance>,
    val recentActivity: List<ActivityItem>
)

data class SubjectPerformance(
    val subject: String,
    val averageScore: Int,
    val lessonsCompleted: Int
)

data class ActivityItem(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val description: String,
    val icon: String,
    val color: Color,
    val timeAgo: String
)

// MARK: - Mock Data
object MockData {
    fun getMockAnalytics(): AnalyticsData {
        return AnalyticsData(
            averageScore = 85,
            completionRate = 92,
            studyTime = 45,
            aiSessions = 23,
            subjectPerformance = listOf(
                SubjectPerformance(
                    subject = "Mathematics",
                    averageScore = 88,
                    lessonsCompleted = 15
                ),
                SubjectPerformance(
                    subject = "Science",
                    averageScore = 82,
                    lessonsCompleted = 12
                ),
                SubjectPerformance(
                    subject = "English",
                    averageScore = 90,
                    lessonsCompleted = 18
                ),
                SubjectPerformance(
                    subject = "History",
                    averageScore = 85,
                    lessonsCompleted = 10
                ),
                SubjectPerformance(
                    subject = "Computer Science",
                    averageScore = 95,
                    lessonsCompleted = 20
                )
            ),
            recentActivity = listOf(
                ActivityItem(
                    title = "Completed AI Lesson",
                    description = "Finished 'Introduction to Algebra'",
                    icon = "📚",
                    color = Color(0xFF4CAF50),
                    timeAgo = "2 hours ago"
                ),
                ActivityItem(
                    title = "Achievement Unlocked",
                    description = "Perfect Attendance - 30 days",
                    icon = "🏆",
                    color = Color(0xFFFF9800),
                    timeAgo = "1 day ago"
                ),
                ActivityItem(
                    title = "Study Session",
                    description = "Studied Physics for 2 hours",
                    icon = "⏰",
                    color = Color(0xFF2196F3),
                    timeAgo = "3 days ago"
                ),
                ActivityItem(
                    title = "AI Conversation",
                    description = "Had a 15-minute AI tutoring session",
                    icon = "🤖",
                    color = Color(0xFF9C27B0),
                    timeAgo = "5 days ago"
                )
            )
        )
    }
}