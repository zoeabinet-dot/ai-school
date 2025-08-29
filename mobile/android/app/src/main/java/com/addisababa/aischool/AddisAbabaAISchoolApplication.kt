package com.addisababa.aischool

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.hilt.work.HiltWorkerFactory
import androidx.work.Configuration
import dagger.hilt.android.HiltAndroidApp
import javax.inject.Inject

@HiltAndroidApp
class AddisAbabaAISchoolApplication : Application(), Configuration.Provider {

    @Inject
    lateinit var workerFactory: HiltWorkerFactory

    override fun onCreate() {
        super.onCreate()
        
        // Initialize AI services
        initializeAIServices()
        
        // Setup notification channels
        createNotificationChannels()
        
        // Initialize analytics
        setupAnalytics()
        
        // Initialize biometric authentication
        setupBiometricAuth()
    }

    override fun getWorkManagerConfiguration(): Configuration {
        return Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()
    }

    private fun initializeAIServices() {
        // Initialize AI services for the school management system
        println("Initializing AI services for Addis Ababa AI School")
        
        // Initialize speech recognition
        // Initialize computer vision
        // Initialize natural language processing
        // Initialize ML Kit components
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

            // Main notification channel
            val mainChannel = NotificationChannel(
                CHANNEL_MAIN,
                "Main Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Main notifications for the AI School app"
                enableLights(true)
                enableVibration(true)
            }

            // AI Lesson notifications
            val aiLessonChannel = NotificationChannel(
                CHANNEL_AI_LESSONS,
                "AI Lesson Notifications",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Notifications for AI lesson updates and progress"
                enableLights(true)
                enableVibration(true)
            }

            // Monitoring notifications
            val monitoringChannel = NotificationChannel(
                CHANNEL_MONITORING,
                "Monitoring Notifications",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Notifications for monitoring and behavior analysis"
                enableLights(true)
                enableVibration(true)
            }

            // Academic notifications
            val academicChannel = NotificationChannel(
                CHANNEL_ACADEMIC,
                "Academic Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Notifications for academic updates and grades"
                enableLights(true)
                enableVibration(true)
            }

            // Family communication notifications
            val familyChannel = NotificationChannel(
                CHANNEL_FAMILY,
                "Family Communication",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Notifications for family communication and updates"
                enableLights(true)
                enableVibration(true)
            }

            // Staff notifications
            val staffChannel = NotificationChannel(
                CHANNEL_STAFF,
                "Staff Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Notifications for staff members"
                enableLights(true)
                enableVibration(true)
            }

            // Create all channels
            notificationManager.createNotificationChannels(
                listOf(
                    mainChannel,
                    aiLessonChannel,
                    monitoringChannel,
                    academicChannel,
                    familyChannel,
                    staffChannel
                )
            )
        }
    }

    private fun setupAnalytics() {
        // Setup analytics and monitoring
        println("Setting up analytics for Addis Ababa AI School")
        
        // Initialize Firebase Analytics
        // Initialize custom analytics
        // Setup crash reporting
    }

    private fun setupBiometricAuth() {
        // Setup biometric authentication
        println("Setting up biometric authentication")
        
        // Check device capabilities
        // Initialize biometric prompt
        // Setup fallback authentication
    }

    companion object {
        const val CHANNEL_MAIN = "main_channel"
        const val CHANNEL_AI_LESSONS = "ai_lessons_channel"
        const val CHANNEL_MONITORING = "monitoring_channel"
        const val CHANNEL_ACADEMIC = "academic_channel"
        const val CHANNEL_FAMILY = "family_channel"
        const val CHANNEL_STAFF = "staff_channel"
    }
}