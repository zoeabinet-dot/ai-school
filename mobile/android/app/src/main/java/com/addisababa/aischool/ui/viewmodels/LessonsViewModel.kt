package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.models.Lesson
import com.addisababa.aischool.data.models.MockData
import com.addisababa.aischool.ui.screens.LessonsUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class LessonsViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow<LessonsUiState>(LessonsUiState.Loading)
    val uiState: StateFlow<LessonsUiState> = _uiState.asStateFlow()
    
    fun loadLessons() {
        viewModelScope.launch {
            _uiState.value = LessonsUiState.Loading
            
            try {
                // Simulate network delay
                delay(1000)
                
                // Load mock data for now
                val lessons = MockData.getMockLessons()
                _uiState.value = LessonsUiState.Success(lessons)
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Unknown error occurred")
            }
        }
    }
    
    fun addLesson(lesson: Lesson) {
        viewModelScope.launch {
            try {
                val currentLessons = (uiState.value as? LessonsUiState.Success)?.lessons
                if (currentLessons != null) {
                    val updatedLessons = currentLessons + lesson
                    _uiState.value = LessonsUiState.Success(updatedLessons)
                }
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Failed to add lesson")
            }
        }
    }
    
    fun deleteLesson(lessonId: String) {
        viewModelScope.launch {
            try {
                val currentLessons = (uiState.value as? LessonsUiState.Success)?.lessons
                if (currentLessons != null) {
                    val updatedLessons = currentLessons.filter { it.id.toString() != lessonId }
                    _uiState.value = LessonsUiState.Success(updatedLessons)
                }
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Failed to delete lesson")
            }
        }
    }
    
    fun updateLesson(lesson: Lesson) {
        viewModelScope.launch {
            try {
                val currentLessons = (uiState.value as? LessonsUiState.Success)?.lessons
                if (currentLessons != null) {
                    val updatedLessons = currentLessons.map { 
                        if (it.id == lesson.id) lesson else it 
                    }
                    _uiState.value = LessonsUiState.Success(updatedLessons)
                }
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Failed to update lesson")
            }
        }
    }
    
    fun filterLessonsBySubject(subject: String) {
        viewModelScope.launch {
            try {
                val currentLessons = (uiState.value as? LessonsUiState.Success)?.lessons
                if (currentLessons != null) {
                    val filteredLessons = if (subject.isBlank()) {
                        currentLessons
                    } else {
                        currentLessons.filter { it.subject.equals(subject, ignoreCase = true) }
                    }
                    _uiState.value = LessonsUiState.Success(filteredLessons)
                }
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Failed to filter lessons")
            }
        }
    }
    
    fun filterLessonsByStatus(status: com.addisababa.aischool.data.models.LessonStatus?) {
        viewModelScope.launch {
            try {
                val currentLessons = (uiState.value as? LessonsUiState.Success)?.lessons
                if (currentLessons != null) {
                    val filteredLessons = if (status == null) {
                        currentLessons
                    } else {
                        currentLessons.filter { it.status == status }
                    }
                    _uiState.value = LessonsUiState.Success(filteredLessons)
                }
            } catch (e: Exception) {
                _uiState.value = LessonsUiState.Error(e.message ?: "Failed to filter lessons")
            }
        }
    }
    
    fun refreshLessons() {
        loadLessons()
    }
}