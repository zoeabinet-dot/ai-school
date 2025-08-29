package com.addisababa.aischool.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.addisababa.aischool.data.models.AILesson
import com.addisababa.aischool.ui.viewmodels.AILessonViewModel

@Composable
fun AILessonScreen(
    modifier: Modifier = Modifier,
    viewModel: AILessonViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.loadLessons()
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("AI Lessons") },
                actions = {
                    IconButton(onClick = { /* TODO: Create new AI lesson */ }) {
                        // Add icon
                    }
                }
            )
        }
    ) { paddingValues ->
        when (uiState) {
            is AILessonUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            is AILessonUiState.Success -> {
                LazyColumn(
                    modifier = modifier.padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(uiState.lessons) { lesson ->
                        AILessonCard(
                            lesson = lesson,
                            onClick = { /* TODO: Navigate to lesson detail */ }
                        )
                    }
                }
            }
            is AILessonUiState.Error -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = uiState.message,
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
        }
    }
}

@Composable
fun AILessonCard(
    lesson: AILesson,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(
                    modifier = Modifier.weight(1f)
                ) {
                    Text(
                        text = lesson.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        text = lesson.subject,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Column(
                    horizontalAlignment = Alignment.End
                ) {
                    Surface(
                        color = when (lesson.difficultyLevel) {
                            DifficultyLevel.BEGINNER -> MaterialTheme.colorScheme.primaryContainer
                            DifficultyLevel.INTERMEDIATE -> MaterialTheme.colorScheme.tertiaryContainer
                            DifficultyLevel.ADVANCED -> MaterialTheme.colorScheme.errorContainer
                        },
                        shape = MaterialTheme.shapes.small
                    ) {
                        Text(
                            text = lesson.difficultyLevel.displayName,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(4.dp))
                    
                    Text(
                        text = "${lesson.estimatedDuration} min",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = lesson.description,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    color = MaterialTheme.colorScheme.primaryContainer,
                    shape = MaterialTheme.shapes.small
                ) {
                    Text(
                        text = "AI Generated",
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
                
                if (lesson.isCompleted) {
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Default.CheckCircle,
                        contentDescription = "Completed",
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
}

// MARK: - UI State
sealed class AILessonUiState {
    object Loading : AILessonUiState()
    data class Success(val lessons: List<AILesson>) : AILessonUiState()
    data class Error(val message: String) : AILessonUiState()
}