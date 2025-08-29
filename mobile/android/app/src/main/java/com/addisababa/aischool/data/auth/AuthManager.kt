package com.addisababa.aischool.data.auth

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.addisababa.aischool.data.models.LoginRequest
import com.addisababa.aischool.data.models.LoginResponse
import com.addisababa.aischool.data.models.User
import com.addisababa.aischool.data.network.RealApiService
import com.addisababa.aischool.data.network.ApiConfig
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.*

class AuthManager private constructor(context: Context) {
    
    companion object {
        private const val PREFS_NAME = "ai_school_auth"
        private const val KEY_AUTH_TOKEN = "auth_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_USER_EMAIL = "user_email"
        private const val KEY_USER_ROLE = "user_role"
        private const val KEY_TOKEN_EXPIRY = "token_expiry"
        
        @Volatile
        private var INSTANCE: AuthManager? = null
        
        fun getInstance(context: Context): AuthManager {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: AuthManager(context).also { INSTANCE = it }
            }
        }
    }
    
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()
    
    private val encryptedPrefs: SharedPreferences = EncryptedSharedPreferences.create(
        context,
        PREFS_NAME,
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
    
    private val _authState = MutableStateFlow<AuthState>(AuthState.Unauthenticated)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()
    
    private val _currentUser = MutableStateFlow<User?>(null)
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()
    
    private var apiService: RealApiService? = null
    
    init {
        // Check if user is already logged in
        checkExistingAuth()
    }
    
    private fun checkExistingAuth() {
        val token = getAuthToken()
        val userId = getUserId()
        
        if (token != null && userId != null && !isTokenExpired()) {
            // Token exists and is valid, restore session
            val user = User(
                id = userId,
                email = getStoredUserEmail() ?: "",
                firstName = "", // Will be fetched from API
                lastName = "",
                role = getStoredUserRole() ?: com.addisababa.aischool.data.models.UserRole.ADMIN
            )
            _currentUser.value = user
            _authState.value = AuthState.Authenticated(user)
            
            // Initialize API service with token
            initializeApiService(token)
        } else {
            // Clear invalid tokens
            clearAuth()
        }
    }
    
    private fun isTokenExpired(): Boolean {
        val expiryTime = getTokenExpiry()
        return expiryTime != null && Date().after(Date(expiryTime))
    }
    
    suspend fun login(email: String, password: String, role: String): Result<LoginResponse> {
        return try {
            _authState.value = AuthState.Loading
            
            val loginRequest = LoginRequest(email, password, role)
            val response = apiService?.login(loginRequest) 
                ?: throw IllegalStateException("API service not initialized")
            
            // Store authentication data
            storeAuthData(response)
            
            // Update state
            _currentUser.value = response.user
            _authState.value = AuthState.Authenticated(response.user)
            
            // Initialize API service with new token
            initializeApiService(response.token)
            
            Result.success(response)
        } catch (e: Exception) {
            _authState.value = AuthState.Error(e.message ?: "Login failed")
            Result.failure(e)
        }
    }
    
    suspend fun logout(): Result<Unit> {
        return try {
            // Call logout API
            apiService?.logout()
            
            // Clear local data
            clearAuth()
            
            // Update state
            _currentUser.value = null
            _authState.value = AuthState.Unauthenticated
            
            Result.success(Unit)
        } catch (e: Exception) {
            // Even if API call fails, clear local data
            clearAuth()
            _currentUser.value = null
            _authState.value = AuthState.Unauthenticated
            Result.failure(e)
        }
    }
    
    suspend fun refreshProfile(): Result<User> {
        return try {
            val response = apiService?.getProfile() 
                ?: throw IllegalStateException("API service not initialized")
            
            _currentUser.value = response.user
            Result.success(response.user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    fun getAuthToken(): String? {
        return encryptedPrefs.getString(KEY_AUTH_TOKEN, null)
    }
    
    fun getRefreshToken(): String? {
        return encryptedPrefs.getString(KEY_REFRESH_TOKEN, null)
    }
    
    fun isAuthenticated(): Boolean {
        val token = getAuthToken()
        return token != null && !isTokenExpired()
    }
    
    private fun storeAuthData(loginResponse: LoginResponse) {
        encryptedPrefs.edit().apply {
            putString(KEY_AUTH_TOKEN, loginResponse.token)
            putString(KEY_REFRESH_TOKEN, loginResponse.token) // For now, using same token
            putString(KEY_USER_ID, loginResponse.user.id)
            putString(KEY_USER_EMAIL, loginResponse.user.email)
            putString(KEY_USER_ROLE, loginResponse.user.role.name)
            
            // Set token expiry to 1 hour from now (matching Django JWT settings)
            val expiryTime = System.currentTimeMillis() + (60 * 60 * 1000)
            putLong(KEY_TOKEN_EXPIRY, expiryTime)
        }.apply()
    }
    
    private fun clearAuth() {
        encryptedPrefs.edit().clear().apply()
        apiService = null
    }
    
    private fun getUserId(): String? {
        return encryptedPrefs.getString(KEY_USER_ID, null)
    }
    
    private fun getStoredUserEmail(): String? {
        return encryptedPrefs.getString(KEY_USER_EMAIL, null)
    }
    
    private fun getStoredUserRole(): com.addisababa.aischool.data.models.UserRole? {
        val roleString = encryptedPrefs.getString(KEY_USER_ROLE, null)
        return roleString?.let { 
            try {
                com.addisababa.aischool.data.models.UserRole.valueOf(it)
            } catch (e: IllegalArgumentException) {
                null
            }
        }
    }
    
    private fun getTokenExpiry(): Long? {
        val expiry = encryptedPrefs.getLong(KEY_TOKEN_EXPIRY, -1)
        return if (expiry > 0) expiry else null
    }
    
    private fun initializeApiService(token: String) {
        apiService = RealApiServiceImpl(ApiConfig.getBaseUrl(), token)
    }
    
    fun getApiService(): RealApiService? {
        return apiService
    }
}

sealed class AuthState {
    object Unauthenticated : AuthState()
    object Loading : AuthState()
    data class Authenticated(val user: User) : AuthState()
    data class Error(val message: String) : AuthState()
}