package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.models.StaffData
import com.addisababa.aischool.data.models.MockData
import com.addisababa.aischool.ui.screens.StaffUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class StaffViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow<StaffUiState>(StaffUiState.Loading)
    val uiState: StateFlow<StaffUiState> = _uiState.asStateFlow()
    
    fun loadStaffData() {
        viewModelScope.launch {
            _uiState.value = StaffUiState.Loading
            
            try {
                // Simulate network delay
                delay(1000)
                
                // Load mock data for now
                val staffData = MockData.getMockStaffData()
                _uiState.value = StaffUiState.Success(staffData)
            } catch (e: Exception) {
                _uiState.value = StaffUiState.Error(e.message ?: "Unknown error occurred")
            }
        }
    }
    
    fun addStaff(staff: com.addisababa.aischool.data.models.Staff) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? StaffUiState.Success)?.staffData
                if (currentData != null) {
                    val updatedStaff = currentData.staff + staff
                    val updatedData = currentData.copy(staff = updatedStaff)
                    _uiState.value = StaffUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = StaffUiState.Error(e.message ?: "Failed to add staff")
            }
        }
    }
    
    fun removeStaff(staffId: String) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? StaffUiState.Success)?.staffData
                if (currentData != null) {
                    val updatedStaff = currentData.staff.filter { it.id.toString() != staffId }
                    val updatedData = currentData.copy(staff = updatedStaff)
                    _uiState.value = StaffUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = StaffUiState.Error(e.message ?: "Failed to remove staff")
            }
        }
    }
    
    fun updateStaffAssignment(assignment: com.addisababa.aischool.data.models.StaffAssignment) {
        viewModelScope.launch {
            try {
                val currentData = (uiState.value as? StaffUiState.Success)?.staffData
                if (currentData != null) {
                    val updatedAssignments = currentData.assignments.map { 
                        if (it.id == assignment.id) assignment else it 
                    }
                    val updatedData = currentData.copy(assignments = updatedAssignments)
                    _uiState.value = StaffUiState.Success(updatedData)
                }
            } catch (e: Exception) {
                _uiState.value = StaffUiState.Error(e.message ?: "Failed to update assignment")
            }
        }
    }
    
    fun refreshStaffData() {
        loadStaffData()
    }
}