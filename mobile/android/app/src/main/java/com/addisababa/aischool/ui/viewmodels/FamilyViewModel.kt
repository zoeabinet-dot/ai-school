package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.models.FamilyData
import com.addisababa.aischool.data.models.MockData
import com.addisababa.aischool.ui.screens.FamilyUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class FamilyViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow<FamilyUiState>(FamilyUiState.Loading)
    val uiState: StateFlow<FamilyUiState> = _uiState.asStateFlow()
    
    fun loadFamilyData() {
        viewModelScope.launch {
            _uiState.value = FamilyUiState.Loading
            
            try {
                // Simulate network delay
                delay(1000)
                
                // Load mock data for now
                val familyData = MockData.getMockFamilyData()
                _uiState.value = FamilyUiState.Success(familyData)
            } catch (e: Exception) {
                _uiState.value = FamilyUiState.Error(e.message ?: "Unknown error occurred")
            }
        }
    }
    
    fun addFamilyMember(member: com.addisababa.aischool.data.models.FamilyMember) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? FamilyUiState.Success)?.familyData
                if (currentData != null) {
                    val updatedMembers = currentData.members + member
                    val updatedData = currentData.copy(members = updatedMembers)
                    _uiState.value = FamilyUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = FamilyUiState.Error(e.message ?: "Failed to add family member")
            }
        }
    }
    
    fun removeFamilyMember(memberId: String) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? FamilyUiState.Success)?.familyData
                if (currentData != null) {
                    val updatedMembers = currentData.members.filter { it.id.toString() != memberId }
                    val updatedData = currentData.copy(members = updatedMembers)
                    _uiState.value = FamilyUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = FamilyUiState.Error(e.message ?: "Failed to remove family member")
            }
        }
    }
    
    fun sendCommunication(communication: com.addisababa.aischool.data.models.FamilyCommunication) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? FamilyUiState.Success)?.familyData
                if (currentData != null) {
                    val updatedCommunications = listOf(communication) + currentData.communications
                    val updatedData = currentData.copy(communications = updatedCommunications)
                    _uiState.value = FamilyUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = FamilyUiState.Error(e.message ?: "Failed to send communication")
            }
        }
    }
    
    fun refreshFamilyData() {
        loadFamilyData()
    }
}