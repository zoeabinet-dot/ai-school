package com.addisababa.aischool.data.network

import com.addisababa.aischool.data.models.*
import kotlinx.coroutines.delay
import retrofit2.http.*

interface ApiService {
    
    // Authentication
    @POST("auth/login/")
    suspend fun login(@Body request: LoginRequest): LoginResponse
    
    @POST("auth/logout/")
    suspend fun logout(): EmptyResponse
    
    @GET("auth/profile/")
    suspend fun getProfile(): UserResponse
    
    // Students
    @GET("students/")
    suspend fun getStudents(): StudentsResponse
    
    @POST("students/")
    suspend fun createStudent(@Body student: Student): StudentResponse
    
    @PUT("students/{id}/")
    suspend fun updateStudent(@Path("id") id: String, @Body student: Student): StudentResponse
    
    @DELETE("students/{id}/")
    suspend fun deleteStudent(@Path("id") id: String): EmptyResponse
    
    // AI Lessons
    @GET("ai-lessons/")
    suspend fun getAILessons(): AILessonsResponse
    
    @POST("ai-lessons/")
    suspend fun createAILesson(@Body lesson: AILesson): AILessonResponse
    
    @PUT("ai-lessons/{id}/")
    suspend fun updateAILesson(@Path("id") id: String, @Body lesson: AILesson): AILessonResponse
    
    @DELETE("ai-lessons/{id}/")
    suspend fun deleteAILesson(@Path("id") id: String): EmptyResponse
    
    // Analytics
    @GET("analytics/")
    suspend fun getAnalytics(@Query("time_range") timeRange: String? = null): AnalyticsResponse
    
    // Monitoring
    @GET("monitoring/")
    suspend fun getMonitoringData(): MonitoringResponse
    
    @POST("monitoring/toggle/")
    suspend fun toggleMonitoring(@Body request: MonitoringToggleRequest): MonitoringResponse
    
    @POST("monitoring/privacy-settings/")
    suspend fun updatePrivacySettings(@Body request: PrivacySettingsRequest): MonitoringResponse
    
    // Families
    @GET("families/")
    suspend fun getFamilyData(): FamilyResponse
    
    @POST("families/members/")
    suspend fun addFamilyMember(@Body member: FamilyMember): FamilyResponse
    
    @DELETE("families/members/{id}/")
    suspend fun removeFamilyMember(@Path("id") id: String): FamilyResponse
    
    // Staff
    @GET("staff/")
    suspend fun getStaffData(): StaffResponse
    
    @POST("staff/")
    suspend fun addStaff(@Body staff: Staff): StaffResponse
    
    @PUT("staff/{id}/")
    suspend fun updateStaff(@Path("id") id: String, @Body staff: Staff): StaffResponse
    
    @DELETE("staff/{id}/")
    suspend fun deleteStaff(@Path("id") id: String): EmptyResponse
    
    // Lessons
    @GET("lessons/")
    suspend fun getLessons(): LessonsResponse
    
    @POST("lessons/")
    suspend fun createLesson(@Body lesson: Lesson): LessonResponse
    
    @PUT("lessons/{id}/")
    suspend fun updateLesson(@Path("id") id: String, @Body lesson: Lesson): LessonResponse
    
    @DELETE("lessons/{id}/")
    suspend fun deleteLesson(@Path("id") id: String): EmptyResponse
}

// Request/Response Models
data class LoginRequest(
    val email: String,
    val password: String,
    val role: String
)

data class LoginResponse(
    val token: String,
    val user: User,
    val message: String
)

data class UserResponse(
    val user: User
)

data class StudentsResponse(
    val students: List<Student>
)

data class StudentResponse(
    val student: Student
)

data class AILessonsResponse(
    val lessons: List<AILesson>
)

data class AILessonResponse(
    val lesson: AILesson
)

data class AnalyticsResponse(
    val analytics: AnalyticsData
)

data class MonitoringResponse(
    val monitoring: MonitoringData
)

data class MonitoringToggleRequest(
    val isActive: Boolean
)

data class PrivacySettingsRequest(
    val faceDetectionEnabled: Boolean,
    val behaviorAnalysisEnabled: Boolean,
    val recordingEnabled: Boolean,
    val alertsEnabled: Boolean
)

data class FamilyResponse(
    val family: FamilyData
)

data class StaffResponse(
    val staff: StaffData
)

data class LessonsResponse(
    val lessons: List<Lesson>
)

data class LessonResponse(
    val lesson: Lesson
)

data class EmptyResponse(
    val message: String
)

// Mock API Service Implementation
class MockApiService : ApiService {
    
    override suspend fun login(request: LoginRequest): LoginResponse {
        delay(1000) // Simulate network delay
        return LoginResponse(
            token = "mock_jwt_token_12345",
            user = User(
                id = "1",
                email = request.email,
                firstName = "Admin",
                lastName = "User",
                role = UserRole.ADMIN
            ),
            message = "Login successful"
        )
    }
    
    override suspend fun logout(): EmptyResponse {
        delay(500)
        return EmptyResponse("Logout successful")
    }
    
    override suspend fun getProfile(): UserResponse {
        delay(800)
        return UserResponse(
            user = User(
                id = "1",
                email = "admin@aischool.com",
                firstName = "Admin",
                lastName = "User",
                role = UserRole.ADMIN
            )
        )
    }
    
    override suspend fun getStudents(): StudentsResponse {
        delay(1000)
        return StudentsResponse(students = MockData.getMockStudents())
    }
    
    override suspend fun createStudent(student: Student): StudentResponse {
        delay(800)
        return StudentResponse(student = student)
    }
    
    override suspend fun updateStudent(id: String, student: Student): StudentResponse {
        delay(800)
        return StudentResponse(student = student)
    }
    
    override suspend fun deleteStudent(id: String): EmptyResponse {
        delay(500)
        return EmptyResponse("Student deleted successfully")
    }
    
    override suspend fun getAILessons(): AILessonsResponse {
        delay(1000)
        return AILessonsResponse(lessons = MockData.getMockAILessons())
    }
    
    override suspend fun createAILesson(lesson: AILesson): AILessonResponse {
        delay(800)
        return AILessonResponse(lesson = lesson)
    }
    
    override suspend fun updateAILesson(id: String, lesson: AILesson): AILessonResponse {
        delay(800)
        return AILessonResponse(lesson = lesson)
    }
    
    override suspend fun deleteAILesson(id: String): EmptyResponse {
        delay(500)
        return EmptyResponse("AI Lesson deleted successfully")
    }
    
    override suspend fun getAnalytics(timeRange: String?): AnalyticsResponse {
        delay(1000)
        return AnalyticsResponse(analytics = MockData.getMockAnalytics())
    }
    
    override suspend fun getMonitoringData(): MonitoringResponse {
        delay(1000)
        return MonitoringResponse(monitoring = MockData.getMockMonitoringData())
    }
    
    override suspend fun toggleMonitoring(request: MonitoringToggleRequest): MonitoringResponse {
        delay(500)
        val currentData = MockData.getMockMonitoringData()
        val updatedData = currentData.copy(isActive = request.isActive)
        return MonitoringResponse(monitoring = updatedData)
    }
    
    override suspend fun updatePrivacySettings(request: PrivacySettingsRequest): MonitoringResponse {
        delay(500)
        val currentData = MockData.getMockMonitoringData()
        val updatedData = currentData.copy(
            faceDetectionEnabled = request.faceDetectionEnabled,
            behaviorAnalysisEnabled = request.behaviorAnalysisEnabled,
            recordingEnabled = request.recordingEnabled,
            alertsEnabled = request.alertsEnabled
        )
        return MonitoringResponse(monitoring = updatedData)
    }
    
    override suspend fun getFamilyData(): FamilyResponse {
        delay(1000)
        return FamilyResponse(family = MockData.getMockFamilyData())
    }
    
    override suspend fun addFamilyMember(member: FamilyMember): FamilyResponse {
        delay(800)
        val currentData = MockData.getMockFamilyData()
        val updatedMembers = currentData.members + member
        val updatedData = currentData.copy(members = updatedMembers)
        return FamilyResponse(family = updatedData)
    }
    
    override suspend fun removeFamilyMember(id: String): FamilyResponse {
        delay(500)
        val currentData = MockData.getMockFamilyData()
        val updatedMembers = currentData.members.filter { it.id.toString() != id }
        val updatedData = currentData.copy(members = updatedMembers)
        return FamilyResponse(family = updatedData)
    }
    
    override suspend fun getStaffData(): StaffResponse {
        delay(1000)
        return StaffResponse(staff = MockData.getMockStaffData())
    }
    
    override suspend fun addStaff(staff: Staff): StaffResponse {
        delay(800)
        val currentData = MockData.getMockStaffData()
        val updatedStaff = currentData.staff + staff
        val updatedData = currentData.copy(staff = updatedStaff)
        return StaffResponse(staff = updatedData)
    }
    
    override suspend fun updateStaff(id: String, staff: Staff): StaffResponse {
        delay(800)
        val currentData = MockData.getMockStaffData()
        val updatedStaff = currentData.staff.map { if (it.id.toString() == id) staff else it }
        val updatedData = currentData.copy(staff = updatedStaff)
        return StaffResponse(staff = updatedData)
    }
    
    override suspend fun deleteStaff(id: String): EmptyResponse {
        delay(500)
        return EmptyResponse("Staff deleted successfully")
    }
    
    override suspend fun getLessons(): LessonsResponse {
        delay(1000)
        return LessonsResponse(lessons = MockData.getMockLessons())
    }
    
    override suspend fun createLesson(lesson: Lesson): LessonResponse {
        delay(800)
        return LessonResponse(lesson = lesson)
    }
    
    override suspend fun updateLesson(id: String, lesson: Lesson): LessonResponse {
        delay(800)
        return LessonResponse(lesson = lesson)
    }
    
    override suspend fun deleteLesson(id: String): EmptyResponse {
        delay(500)
        return EmptyResponse("Lesson deleted successfully")
    }
}