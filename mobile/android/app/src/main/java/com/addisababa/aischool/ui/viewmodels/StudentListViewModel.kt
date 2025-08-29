package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.models.MockData
import com.addisababa.aischool.data.models.Student
import com.addisababa.aischool.ui.screens.StudentListUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class StudentListViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow<StudentListUiState>(StudentListUiState.Loading)
    val uiState: StateFlow<StudentListUiState> = _uiState.asStateFlow()
    
    fun loadStudents() {
        viewModelScope.launch {
            _uiState.value = StudentListUiState.Loading
            
            try {
                // Simulate network delay
                delay(1000)
                
                // Load mock data for now
                val students = MockData.getMockStudents()
                _uiState.value = StudentListUiState.Success(students)
            } catch (e: Exception) {
                _uiState.value = StudentListUiState.Error(e.message ?: "Unknown error occurred")
            }
        }
    }
    
    fun addStudent(student: Student) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentStudents = (uiState.value as? StudentListUiState.Success)?.students ?: emptyList()
                val updatedStudents = currentStudents + student
                _uiState.value = StudentListUiState.Success(updatedStudents)
            } catch (e: Exception) {
                _uiState.value = StudentListUiState.Error(e.message ?: "Failed to add student")
            }
        }
    }
    
    fun deleteStudent(studentId: String) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentStudents = (uiState.value as? StudentListUiState.Success)?.students ?: emptyList()
                val updatedStudents = currentStudents.filter { it.id.toString() != studentId }
                _uiState.value = StudentListUiState.Success(updatedStudents)
            } catch (e: Exception) {
                _uiState.value = StudentListUiState.Error(e.message ?: "Failed to delete student")
            }
        }
    }
    
    fun updateStudent(student: Student) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentStudents = (uiState.value as? StudentListUiState.Success)?.students ?: emptyList()
                val updatedStudents = currentStudents.map { 
                    if (it.id == student.id) student else it 
                }
                _uiState.value = StudentListUiState.Success(updatedStudents)
            } catch (e: Exception) {
                _uiState.value = StudentListUiState.Error(e.message ?: "Failed to update student")
            }
        }
    }
}