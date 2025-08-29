package com.addisababa.aischool.data.network

import com.addisababa.aischool.data.models.*
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

interface RealApiService {
    
    // Authentication
    @POST("api/v1/accounts/login/")
    suspend fun login(@Body request: LoginRequest): LoginResponse
    
    @POST("api/v1/accounts/logout/")
    suspend fun logout(): EmptyResponse
    
    @GET("api/v1/accounts/profile/")
    suspend fun getProfile(): UserResponse
    
    // Students
    @GET("api/v1/students/")
    suspend fun getStudents(
        @Query("grade_level") gradeLevel: String? = null,
        @Query("subject") subject: String? = null,
        @Query("performance_level") performanceLevel: String? = null,
        @Query("family_id") familyId: String? = null
    ): StudentsResponse
    
    @POST("api/v1/students/")
    suspend fun createStudent(@Body student: Student): StudentResponse
    
    @PUT("api/v1/students/{id}/")
    suspend fun updateStudent(@Path("id") id: String, @Body student: Student): StudentResponse
    
    @DELETE("api/v1/students/{id}/")
    suspend fun deleteStudent(@Path("id") id: String): EmptyResponse
    
    // AI Lessons
    @GET("api/v1/ai-teacher/lessons/")
    suspend fun getAILessons(): AILessonsResponse
    
    @POST("api/v1/ai-teacher/lessons/")
    suspend fun createAILesson(@Body lesson: AILesson): AILessonResponse
    
    @PUT("api/v1/ai-teacher/lessons/{id}/")
    suspend fun updateAILesson(@Path("id") id: String, @Body lesson: AILesson): AILessonResponse
    
    @DELETE("api/v1/ai-teacher/lessons/{id}/")
    suspend fun deleteAILesson(@Path("id") id: String): EmptyResponse
    
    // Analytics
    @GET("api/v1/analytics/")
    suspend fun getAnalytics(@Query("time_range") timeRange: String? = null): AnalyticsResponse
    
    // Monitoring
    @GET("api/v1/monitoring/")
    suspend fun getMonitoringData(): MonitoringResponse
    
    @POST("api/v1/monitoring/toggle/")
    suspend fun toggleMonitoring(@Body request: MonitoringToggleRequest): MonitoringResponse
    
    @POST("api/v1/monitoring/privacy-settings/")
    suspend fun updatePrivacySettings(@Body request: PrivacySettingsRequest): MonitoringResponse
    
    // Families
    @GET("api/v1/families/")
    suspend fun getFamilyData(): FamilyResponse
    
    @POST("api/v1/families/members/")
    suspend fun addFamilyMember(@Body member: FamilyMember): FamilyResponse
    
    @DELETE("api/v1/families/members/{id}/")
    suspend fun removeFamilyMember(@Path("id") id: String): FamilyResponse
    
    // Staff
    @GET("api/v1/staff/")
    suspend fun getStaffData(): StaffResponse
    
    @POST("api/v1/staff/")
    suspend fun addStaff(@Body staff: Staff): StaffResponse
    
    @PUT("api/v1/staff/{id}/")
    suspend fun updateStaff(@Path("id") id: String, @Body staff: Staff): StaffResponse
    
    @DELETE("api/v1/staff/{id}/")
    suspend fun deleteStaff(@Path("id") id: String): EmptyResponse
    
    // Lessons
    @GET("api/v1/lessons/")
    suspend fun getLessons(): LessonsResponse
    
    @POST("api/v1/lessons/")
    suspend fun createLesson(@Body lesson: Lesson): LessonResponse
    
    @PUT("api/v1/lessons/{id}/")
    suspend fun updateLesson(@Path("id") id: String, @Body lesson: Lesson): LessonResponse
    
    @DELETE("api/v1/lessons/{id}/")
    suspend fun deleteLesson(@Path("id") id: String): EmptyResponse
}

// Real API Service Implementation
class RealApiServiceImpl(
    private val baseUrl: String,
    private val authToken: String? = null
) : RealApiService {
    
    private val retrofit: Retrofit by lazy {
        val client = OkHttpClient.Builder()
            .addInterceptor(createAuthInterceptor())
            .addInterceptor(createLoggingInterceptor())
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
        
        Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    private val apiService: RealApiService by lazy {
        retrofit.create(RealApiService::class.java)
    }
    
    private fun createAuthInterceptor() = okhttp3.Interceptor { chain ->
        val originalRequest = chain.request()
        val newRequest = if (authToken != null) {
            originalRequest.newBuilder()
                .header("Authorization", "Bearer $authToken")
                .build()
        } else {
            originalRequest
        }
        chain.proceed(newRequest)
    }
    
    private fun createLoggingInterceptor() = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    // Authentication
    override suspend fun login(request: LoginRequest): LoginResponse {
        return apiService.login(request)
    }
    
    override suspend fun logout(): EmptyResponse {
        return apiService.logout()
    }
    
    override suspend fun getProfile(): UserResponse {
        return apiService.getProfile()
    }
    
    // Students
    override suspend fun getStudents(
        gradeLevel: String?,
        subject: String?,
        performanceLevel: String?,
        familyId: String?
    ): StudentsResponse {
        return apiService.getStudents(gradeLevel, subject, performanceLevel, familyId)
    }
    
    override suspend fun createStudent(student: Student): StudentResponse {
        return apiService.createStudent(student)
    }
    
    override suspend fun updateStudent(id: String, student: Student): StudentResponse {
        return apiService.updateStudent(id, student)
    }
    
    override suspend fun deleteStudent(id: String): EmptyResponse {
        return apiService.deleteStudent(id)
    }
    
    // AI Lessons
    override suspend fun getAILessons(): AILessonsResponse {
        return apiService.getAILessons()
    }
    
    override suspend fun createAILesson(lesson: AILesson): AILessonResponse {
        return apiService.createAILesson(lesson)
    }
    
    override suspend fun updateAILesson(id: String, lesson: AILesson): AILessonResponse {
        return apiService.updateAILesson(id, lesson)
    }
    
    override suspend fun deleteAILesson(id: String): EmptyResponse {
        return apiService.deleteAILesson(id)
    }
    
    // Analytics
    override suspend fun getAnalytics(timeRange: String?): AnalyticsResponse {
        return apiService.getAnalytics(timeRange)
    }
    
    // Monitoring
    override suspend fun getMonitoringData(): MonitoringResponse {
        return apiService.getMonitoringData()
    }
    
    override suspend fun toggleMonitoring(request: MonitoringToggleRequest): MonitoringResponse {
        return apiService.toggleMonitoring(request)
    }
    
    override suspend fun updatePrivacySettings(request: PrivacySettingsRequest): MonitoringResponse {
        return apiService.updatePrivacySettings(request)
    }
    
    // Families
    override suspend fun getFamilyData(): FamilyResponse {
        return apiService.getFamilyData()
    }
    
    override suspend fun addFamilyMember(member: FamilyMember): FamilyResponse {
        return apiService.addFamilyMember(member)
    }
    
    override suspend fun removeFamilyMember(id: String): FamilyResponse {
        return apiService.removeFamilyMember(id)
    }
    
    // Staff
    override suspend fun getStaffData(): StaffResponse {
        return apiService.getStaffData()
    }
    
    override suspend fun addStaff(staff: Staff): StaffResponse {
        return apiService.addStaff(staff)
    }
    
    override suspend fun updateStaff(id: String, staff: Staff): StaffResponse {
        return apiService.updateStaff(id, staff)
    }
    
    override suspend fun deleteStaff(id: String): EmptyResponse {
        return apiService.deleteStaff(id)
    }
    
    // Lessons
    override suspend fun getLessons(): LessonsResponse {
        return apiService.getLessons()
    }
    
    override suspend fun createLesson(lesson: Lesson): LessonResponse {
        return apiService.createLesson(lesson)
    }
    
    override suspend fun updateLesson(id: String, lesson: Lesson): LessonResponse {
        return apiService.updateLesson(id, lesson)
    }
    
    override suspend fun deleteLesson(id: String): EmptyResponse {
        return apiService.deleteLesson(id)
    }
}

// API Configuration
object ApiConfig {
    const val BASE_URL = "http://10.0.2.2:8000/" // Android emulator localhost
    const val PRODUCTION_BASE_URL = "https://api.addisababa-aischool.com/"
    
    fun getBaseUrl(isProduction: Boolean = false): String {
        return if (isProduction) PRODUCTION_BASE_URL else BASE_URL
    }
}