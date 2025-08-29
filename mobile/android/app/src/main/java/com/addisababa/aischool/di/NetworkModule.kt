package com.addisababa.aischool.di

import android.content.Context
import com.addisababa.aischool.data.auth.AuthManager
import com.addisababa.aischool.data.network.ApiService
import com.addisababa.aischool.data.network.MockApiService
import com.addisababa.aischool.data.network.RealApiService
import com.addisababa.aischool.data.network.RealApiServiceImpl
import com.addisababa.aischool.data.network.ApiConfig
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideAuthManager(@ApplicationContext context: Context): AuthManager {
        return AuthManager.getInstance(context)
    }
    
    @Provides
    @Singleton
    fun provideApiService(
        authManager: AuthManager,
        @ApplicationContext context: Context
    ): ApiService {
        // Check if we should use real API or mock
        val useRealApi = true // TODO: Make this configurable via build config
        
        return if (useRealApi) {
            // Return a wrapper that can switch between real and mock
            RealApiServiceWrapper(authManager)
        } else {
            MockApiService()
        }
    }
    
    @Provides
    @Singleton
    fun provideRealApiService(authManager: AuthManager): RealApiService? {
        return authManager.getApiService()
    }
}

// Wrapper class that implements ApiService interface
class RealApiServiceWrapper(
    private val authManager: AuthManager
) : ApiService {
    
    private fun getRealService(): RealApiService? {
        return authManager.getApiService()
    }
    
    private fun getMockService(): MockApiService {
        return MockApiService()
    }
    
    override suspend fun login(request: com.addisababa.aischool.data.network.LoginRequest): com.addisababa.aischool.data.network.LoginResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.login(request)
            } catch (e: Exception) {
                // Fallback to mock if real API fails
                getMockService().login(request)
            }
        } else {
            getMockService().login(request)
        }
    }
    
    override suspend fun logout(): com.addisababa.aischool.data.network.EmptyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.logout()
            } catch (e: Exception) {
                getMockService().logout()
            }
        } else {
            getMockService().logout()
        }
    }
    
    override suspend fun getProfile(): com.addisababa.aischool.data.network.UserResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getProfile()
            } catch (e: Exception) {
                getMockService().getProfile()
            }
        } else {
            getMockService().getProfile()
        }
    }
    
    override suspend fun getStudents(): com.addisababa.aischool.data.network.StudentsResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getStudents()
            } catch (e: Exception) {
                getMockService().getStudents()
            }
        } else {
            getMockService().getStudents()
        }
    }
    
    override suspend fun createStudent(student: com.addisababa.aischool.data.models.Student): com.addisababa.aischool.data.network.StudentResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.createStudent(student)
            } catch (e: Exception) {
                getMockService().createStudent(student)
            }
        } else {
            getMockService().createStudent(student)
        }
    }
    
    override suspend fun updateStudent(id: String, student: com.addisababa.aischool.data.models.Student): com.addisababa.aischool.data.network.StudentResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.updateStudent(id, student)
            } catch (e: Exception) {
                getMockService().updateStudent(id, student)
            }
        } else {
            getMockService().updateStudent(id, student)
        }
    }
    
    override suspend fun deleteStudent(id: String): com.addisababa.aischool.data.network.EmptyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.deleteStudent(id)
            } catch (e: Exception) {
                getMockService().deleteStudent(id)
            }
        } else {
            getMockService().deleteStudent(id)
        }
    }
    
    override suspend fun getAILessons(): com.addisababa.aischool.data.network.AILessonsResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getAILessons()
            } catch (e: Exception) {
                getMockService().getAILessons()
            }
        } else {
            getMockService().getAILessons()
        }
    }
    
    override suspend fun createAILesson(lesson: com.addisababa.aischool.data.models.AILesson): com.addisababa.aischool.data.network.AILessonResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.createAILesson(lesson)
            } catch (e: Exception) {
                getMockService().createAILesson(lesson)
            }
        } else {
            getMockService().createAILesson(lesson)
        }
    }
    
    override suspend fun updateAILesson(id: String, lesson: com.addisababa.aischool.data.models.AILesson): com.addisababa.aischool.data.network.AILessonResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.updateAILesson(id, lesson)
            } catch (e: Exception) {
                getMockService().updateAILesson(id, lesson)
            }
        } else {
            getMockService().updateAILesson(id, lesson)
        }
    }
    
    override suspend fun deleteAILesson(id: String): com.addisababa.aischool.data.network.EmptyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.deleteAILesson(id)
            } catch (e: Exception) {
                getMockService().deleteAILesson(id)
            }
        } else {
            getMockService().deleteAILesson(id)
        }
    }
    
    override suspend fun getAnalytics(timeRange: String?): com.addisababa.aischool.data.network.AnalyticsResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getAnalytics(timeRange)
            } catch (e: Exception) {
                getMockService().getAnalytics(timeRange)
            }
        } else {
            getMockService().getAnalytics(timeRange)
        }
    }
    
    override suspend fun getMonitoringData(): com.addisababa.aischool.data.network.MonitoringResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getMonitoringData()
            } catch (e: Exception) {
                getMockService().getMonitoringData()
            }
        } else {
            getMockService().getMonitoringData()
        }
    }
    
    override suspend fun toggleMonitoring(request: com.addisababa.aischool.data.network.MonitoringToggleRequest): com.addisababa.aischool.data.network.MonitoringResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.toggleMonitoring(request)
            } catch (e: Exception) {
                getMockService().toggleMonitoring(request)
            }
        } else {
            getMockService().toggleMonitoring(request)
        }
    }
    
    override suspend fun updatePrivacySettings(request: com.addisababa.aischool.data.network.PrivacySettingsRequest): com.addisababa.aischool.data.network.MonitoringResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.updatePrivacySettings(request)
            } catch (e: Exception) {
                getMockService().updatePrivacySettings(request)
            }
        } else {
            getMockService().updatePrivacySettings(request)
        }
    }
    
    override suspend fun getFamilyData(): com.addisababa.aischool.data.network.FamilyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getFamilyData()
            } catch (e: Exception) {
                getMockService().getFamilyData()
            }
        } else {
            getMockService().getFamilyData()
        }
    }
    
    override suspend fun addFamilyMember(member: com.addisababa.aischool.data.models.FamilyMember): com.addisababa.aischool.data.network.FamilyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.addFamilyMember(member)
            } catch (e: Exception) {
                getMockService().addFamilyMember(member)
            }
        } else {
            getMockService().addFamilyMember(member)
        }
    }
    
    override suspend fun removeFamilyMember(id: String): com.addisababa.aischool.data.network.FamilyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.removeFamilyMember(id)
            } catch (e: Exception) {
                getMockService().removeFamilyMember(id)
            }
        } else {
            getMockService().removeFamilyMember(id)
        }
    }
    
    override suspend fun getStaffData(): com.addisababa.aischool.data.network.StaffResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getStaffData()
            } catch (e: Exception) {
                getMockService().getStaffData()
            }
        } else {
            getMockService().getStaffData()
        }
    }
    
    override suspend fun addStaff(staff: com.addisababa.aischool.data.models.Staff): com.addisababa.aischool.data.network.StaffResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.addStaff(staff)
            } catch (e: Exception) {
                getMockService().addStaff(staff)
            }
        } else {
            getMockService().addStaff(staff)
        }
    }
    
    override suspend fun updateStaff(id: String, staff: com.addisababa.aischool.data.models.Staff): com.addisababa.aischool.data.network.StaffResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.updateStaff(id, staff)
            } catch (e: Exception) {
                getMockService().updateStaff(id, staff)
            }
        } else {
            getMockService().updateStaff(id, staff)
        }
    }
    
    override suspend fun deleteStaff(id: String): com.addisababa.aischool.data.network.EmptyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.deleteStaff(id)
            } catch (e: Exception) {
                getMockService().deleteStaff(id)
            }
        } else {
            getMockService().deleteStaff(id)
        }
    }
    
    override suspend fun getLessons(): com.addisababa.aischool.data.network.LessonsResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.getLessons()
            } catch (e: Exception) {
                getMockService().getLessons()
            }
        } else {
            getMockService().getLessons()
        }
    }
    
    override suspend fun createLesson(lesson: com.addisababa.aischool.data.models.Lesson): com.addisababa.aischool.data.network.LessonResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.createLesson(lesson)
            } catch (e: Exception) {
                getMockService().createLesson(lesson)
            }
        } else {
            getMockService().createLesson(lesson)
        }
    }
    
    override suspend fun updateLesson(id: String, lesson: com.addisababa.aischool.data.models.Lesson): com.addisababa.aischool.data.network.LessonResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.updateLesson(id, lesson)
            } catch (e: Exception) {
                getMockService().updateLesson(id, lesson)
            }
        } else {
            getMockService().updateLesson(id, lesson)
        }
    }
    
    override suspend fun deleteLesson(id: String): com.addisababa.aischool.data.network.EmptyResponse {
        val realService = getRealService()
        return if (realService != null) {
            try {
                realService.deleteLesson(id)
            } catch (e: Exception) {
                getMockService().deleteLesson(id)
            }
        } else {
            getMockService().deleteLesson(id)
        }
    }
}