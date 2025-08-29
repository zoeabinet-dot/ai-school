package com.addisababa.aischool.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.addisababa.aischool.data.models.AILesson
import com.addisababa.aischool.data.models.MockData
import com.addisababa.aischool.ui.screens.AILessonUiState
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class AILessonViewModel : ViewModel() {
    
    private val _uiState = MutableStateFlow<AILessonUiState>(AILessonUiState.Loading)
    val uiState: StateFlow<AILessonUiState> = _uiState.asStateFlow()
    
    fun loadLessons() {
        viewModelScope.launch {
            _uiState.value = AILessonUiState.Loading
            
            try {
                // Simulate network delay
                delay(1000)
                
                // Load mock data for now
                val lessons = MockData.getMockAILessons()
                _uiState.value = AILessonUiState.Success(lessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Unknown error occurred")
            }
        }
    }
    
    fun createLesson(lesson: AILesson) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentLessons = (uiState.value as? AILessonUiState.Success)?.lessons ?: emptyList()
                val updatedLessons = currentLessons + lesson
                _uiState.value = AILessonUiState.Success(updatedLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to create lesson")
            }
        }
    }
    
    fun deleteLesson(lessonId: String) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentLessons = (uiState.value as? AILessonUiState.Success)?.lessons ?: emptyList()
                val updatedLessons = currentLessons.filter { it.id.toString() != lessonId }
                _uiState.value = AILessonUiState.Success(updatedLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to delete lesson")
            }
        }
    }
    
    fun updateLesson(lesson: AILesson) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentLessons = (uiState.value as? AILessonUiState.Success)?.lessons ?: emptyList()
                val updatedLessons = currentLessons.map { 
                    if (it.id == lesson.id) lesson else it 
                }
                _uiState.value = AILessonUiState.Success(updatedLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to update lesson")
            }
        }
    }
    
    fun markLessonAsCompleted(lessonId: String) {
        viewModelScope.launch {
            try {
                // TODO: Implement actual API call
                val currentLessons = (uiState.value as? AILessonUiState.Success)?.lessons ?: emptyList()
                val updatedLessons = currentLessons.map { 
                    if (it.id.toString() == lessonId) it.copy(isCompleted = true) else it 
                }
                _uiState.value = AILessonUiState.Success(updatedLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to mark lesson as completed")
            }
        }
    }
    
    fun filterLessonsByDifficulty(difficultyLevel: com.addisababa.aischool.data.models.DifficultyLevel?) {
        viewModelScope.launch {
            try {
                val allLessons = MockData.getMockAILessons()
                val filteredLessons = if (difficultyLevel != null) {
                    allLessons.filter { it.difficultyLevel == difficultyLevel }
                } else {
                    allLessons
                }
                _uiState.value = AILessonUiState.Success(filteredLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to filter lessons")
            }
        }
    }
    
    fun searchLessons(query: String) {
        viewModelScope.launch {
            try {
                val allLessons = MockData.getMockAILessons()
                val filteredLessons = if (query.isNotEmpty()) {
                    allLessons.filter { 
                        it.title.contains(query, ignoreCase = true) ||
                        it.subject.contains(query, ignoreCase = true) ||
                        it.description.contains(query, ignoreCase = true)
                    }
                } else {
                    allLessons
                }
                _uiState.value = AILessonUiState.Success(filteredLessons)
            } catch (e: Exception) {
                _uiState.value = AILessonUiState.Error(e.message ?: "Failed to search lessons")
            }
        }
    }
}