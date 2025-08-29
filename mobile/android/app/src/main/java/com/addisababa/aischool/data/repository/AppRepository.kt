package com.addisababa.aischool.data.repository

import com.addisababa.aischool.data.models.*
import com.addisababa.aischool.data.network.ApiService
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AppRepository @Inject constructor(
    private val apiService: ApiService
) {
    
    // Authentication
    suspend fun login(email: String, password: String, role: String): Result<LoginResponse> {
        return try {
            val response = apiService.login(LoginRequest(email, password, role))
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun logout(): Result<EmptyResponse> {
        return try {
            val response = apiService.logout()
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getProfile(): Result<UserResponse> {
        return try {
            val response = apiService.getProfile()
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Students
    fun getStudents(): Flow<Result<List<Student>>> = flow {
        try {
            val response = apiService.getStudents()
            emit(Result.success(response.students))
        } catch (e: Exception) {
            emit(Result.failure(e))
        }
    }
    
    suspend fun createStudent(student: Student): Result<Student> {
        return try {
            val response = apiService.createStudent(student)
            Result.success(response.student)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updateStudent(id: String, student: Student): Result<Student> {
        return try {
            val response = apiService.updateStudent(id, student)
            Result.success(response.student)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteStudent(id: String): Result<String> {
        return try {
            val response = apiService.deleteStudent(id)
            Result.success(response.message)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // AI Lessons
    fun getAILessons(): Flow<Result<List<AILesson>>> = flow {
        try {
            val response = apiService.getAILessons()
            emit(Result.success(response.lessons))
        } catch (e: Exception) {
            emit(Result.failure(e))
        }
    }
    
    suspend fun createAILesson(lesson: AILesson): Result<AILesson> {
        return try {
            val response = apiService.createAILesson(lesson)
            Result.success(response.lesson)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updateAILesson(id: String, lesson: AILesson): Result<AILesson> {
        return try {
            val response = apiService.updateAILesson(id, lesson)
            Result.success(response.lesson)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteAILesson(id: String): Result<String> {
        return try {
            val response = apiService.deleteAILesson(id)
            Result.success(response.message)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Analytics
    suspend fun getAnalytics(timeRange: String? = null): Result<AnalyticsData> {
        return try {
            val response = apiService.getAnalytics(timeRange)
            Result.success(response.analytics)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Monitoring
    suspend fun getMonitoringData(): Result<MonitoringData> {
        return try {
            val response = apiService.getMonitoringData()
            Result.success(response.monitoring)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun toggleMonitoring(isActive: Boolean): Result<MonitoringData> {
        return try {
            val response = apiService.toggleMonitoring(MonitoringToggleRequest(isActive))
            Result.success(response.monitoring)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updatePrivacySettings(
        faceDetectionEnabled: Boolean,
        behaviorAnalysisEnabled: Boolean,
        recordingEnabled: Boolean,
        alertsEnabled: Boolean
    ): Result<MonitoringData> {
        return try {
            val request = PrivacySettingsRequest(
                faceDetectionEnabled,
                behaviorAnalysisEnabled,
                recordingEnabled,
                alertsEnabled
            )
            val response = apiService.updatePrivacySettings(request)
            Result.success(response.monitoring)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Families
    suspend fun getFamilyData(): Result<FamilyData> {
        return try {
            val response = apiService.getFamilyData()
            Result.success(response.family)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun addFamilyMember(member: FamilyMember): Result<FamilyData> {
        return try {
            val response = apiService.addFamilyMember(member)
            Result.success(response.family)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun removeFamilyMember(id: String): Result<FamilyData> {
        return try {
            val response = apiService.removeFamilyMember(id)
            Result.success(response.family)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Staff
    suspend fun getStaffData(): Result<StaffData> {
        return try {
            val response = apiService.getStaffData()
            Result.success(response.staff)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun addStaff(staff: Staff): Result<StaffData> {
        return try {
            val response = apiService.addStaff(staff)
            Result.success(response.staff)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updateStaff(id: String, staff: Staff): Result<StaffData> {
        return try {
            val response = apiService.updateStaff(id, staff)
            Result.success(response.staff)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteStaff(id: String): Result<String> {
        return try {
            val response = apiService.deleteStaff(id)
            Result.success(response.message)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Lessons
    fun getLessons(): Flow<Result<List<Lesson>>> = flow {
        try {
            val response = apiService.getLessons()
            emit(Result.success(response.lessons))
        } catch (e: Exception) {
            emit(Result.failure(e))
        }
    }
    
    suspend fun createLesson(lesson: Lesson): Result<Lesson> {
        return try {
            val response = apiService.createLesson(lesson)
            Result.success(response.lesson)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updateLesson(id: String, lesson: Lesson): Result<Lesson> {
        return try {
            val response = apiService.updateLesson(id, lesson)
            Result.success(response.lesson)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteLesson(id: String): Result<String> {
        return try {
            val response = apiService.deleteLesson(id)
            Result.success(response.message)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}