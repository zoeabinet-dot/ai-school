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
import com.addisababa.aischool.data.models.Student
import com.addisababa.aischool.ui.viewmodels.StudentListViewModel

@Composable
fun StudentListScreen(
    modifier: Modifier = Modifier,
    viewModel: StudentListViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.loadStudents()
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Students") },
                actions = {
                    IconButton(onClick = { /* TODO: Add student */ }) {
                        // Add icon
                    }
                }
            )
        }
    ) { paddingValues ->
        when (uiState) {
            is StudentListUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            is StudentListUiState.Success -> {
                LazyColumn(
                    modifier = modifier.padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(uiState.students) { student ->
                        StudentCard(
                            student = student,
                            onClick = { /* TODO: Navigate to student detail */ }
                        )
                    }
                }
            }
            is StudentListUiState.Error -> {
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
fun StudentCard(
    student: Student,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Student Avatar
            Surface(
                modifier = Modifier.size(50.dp),
                shape = MaterialTheme.shapes.circular,
                color = MaterialTheme.colorScheme.primaryContainer
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = student.initials,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            // Student Info
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = student.fullName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = student.grade,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "Age: ${student.age}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            // Status Badge
            Surface(
                color = when (student.status) {
                    StudentStatus.ACTIVE -> MaterialTheme.colorScheme.primaryContainer
                    StudentStatus.INACTIVE -> MaterialTheme.colorScheme.errorContainer
                    StudentStatus.PENDING -> MaterialTheme.colorScheme.tertiaryContainer
                    else -> MaterialTheme.colorScheme.surfaceVariant
                },
                shape = MaterialTheme.shapes.small
            ) {
                Text(
                    text = student.status.displayName,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall
                )
            }
        }
    }
}

// MARK: - UI State
sealed class StudentListUiState {
    object Loading : StudentListUiState()
    data class Success(val students: List<Student>) : StudentListUiState()
    data class Error(val message: String) : StudentListUiState()
}