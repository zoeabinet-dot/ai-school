package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.auth.AuthManager
import com.addisababa.aischool.ui.screens.LoginUiState
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val authManager: AuthManager
) : ViewModel() {
    
    private val _uiState = MutableStateFlow<LoginUiState>(LoginUiState.Initial)
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()
    
    fun login(email: String, password: String, role: String) {
        viewModelScope.launch {
            _uiState.value = LoginUiState.Loading
            
            try {
                val result = authManager.login(email, password, role)
                
                result.fold(
                    onSuccess = {
                        _uiState.value = LoginUiState.Success
                    },
                    onFailure = { exception ->
                        _uiState.value = LoginUiState.Error(
                            exception.message ?: "Login failed. Please check your credentials."
                        )
                    }
                )
            } catch (e: Exception) {
                _uiState.value = LoginUiState.Error(
                    "Network error: ${e.message ?: "Unable to connect to server"}"
                )
            }
        }
    }
    
    fun resetState() {
        _uiState.value = LoginUiState.Initial
    }
    
    fun isAuthenticated(): Boolean {
        return authManager.isAuthenticated()
    }
}