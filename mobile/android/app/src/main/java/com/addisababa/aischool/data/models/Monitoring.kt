package com.addisababa.aischool.data.models

import androidx.compose.ui.graphics.Color
import java.util.UUID

data class MonitoringData(
    val isActive: Boolean,
    val faceDetectionEnabled: Boolean,
    val behaviorAnalysisEnabled: Boolean,
    val recordingEnabled: Boolean,
    val alertsEnabled: Boolean,
    val recentSessions: List<MonitoringSession>,
    val behaviorAnalytics: BehaviorAnalytics,
    val recentAlerts: List<MonitoringAlert>
)

data class MonitoringSession(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val duration: String,
    val status: SessionStatus,
    val date: String
)

data class BehaviorAnalytics(
    val attentionScore: Int,
    val engagementScore: Int,
    val focusTime: Int,
    val distractions: Int
)

data class MonitoringAlert(
    val id: UUID = UUID.randomUUID(),
    val title: String,
    val description: String,
    val severity: AlertSeverity,
    val icon: String,
    val timeAgo: String
)

enum class SessionStatus(val displayName: String) {
    ACTIVE("Active"),
    COMPLETED("Completed"),
    INTERRUPTED("Interrupted")
}

enum class AlertSeverity(val color: Color) {
    INFO(Color(0xFF2196F3)),
    WARNING(Color(0xFFFF9800)),
    CRITICAL(Color(0xFFF44336))
}

// MARK: - Mock Data
object MockData {
    fun getMockMonitoringData(): MonitoringData {
        return MonitoringData(
            isActive = true,
            faceDetectionEnabled = true,
            behaviorAnalysisEnabled = true,
            recordingEnabled = false,
            alertsEnabled = true,
            recentSessions = listOf(
                MonitoringSession(
                    title = "Study Session",
                    duration = "45 min",
                    status = SessionStatus.COMPLETED,
                    date = "Today, 2:30 PM"
                ),
                MonitoringSession(
                    title = "AI Lesson",
                    duration = "30 min",
                    status = SessionStatus.COMPLETED,
                    date = "Today, 10:15 AM"
                ),
                MonitoringSession(
                    title = "Homework",
                    duration = "20 min",
                    status = SessionStatus.INTERRUPTED,
                    date = "Yesterday, 8:45 PM"
                )
            ),
            behaviorAnalytics = BehaviorAnalytics(
                attentionScore = 85,
                engagementScore = 78,
                focusTime = 45,
                distractions = 3
            ),
            recentAlerts = listOf(
                MonitoringAlert(
                    title = "Low Attention",
                    description = "Attention level dropped below 60%",
                    severity = AlertSeverity.WARNING,
                    icon = "👁️",
                    timeAgo = "5 min ago"
                ),
                MonitoringAlert(
                    title = "Distraction Detected",
                    description = "Multiple distractions detected",
                    severity = AlertSeverity.INFO,
                    icon = "⚠️",
                    timeAgo = "15 min ago"
                ),
                MonitoringAlert(
                    title = "Session Completed",
                    description = "Study session completed successfully",
                    severity = AlertSeverity.INFO,
                    icon = "✅",
                    timeAgo = "1 hour ago"
                )
            )
        )
    }
}