package com.addisababa.aischool.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.addisababa.aischool.data.models.StaffData
import com.addisababa.aischool.ui.viewmodels.StaffViewModel

@Composable
fun StaffScreen(
    modifier: Modifier = Modifier,
    viewModel: StaffViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.loadStaffData()
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Staff") },
                actions = {
                    IconButton(onClick = { /* TODO: Add staff */ }) {
                        // Add icon
                    }
                }
            )
        }
    ) { paddingValues ->
        when (uiState) {
            is StaffUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            is StaffUiState.Success -> {
                LazyColumn(
                    modifier = modifier.padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    item {
                        StaffOverviewCard(staffData = uiState.staffData)
                    }
                    
                    item {
                        StaffListCard(staffData = uiState.staffData)
                    }
                    
                    item {
                        AssignmentsCard(staffData = uiState.staffData)
                    }
                    
                    item {
                        PerformanceCard(staffData = uiState.staffData)
                    }
                }
            }
            is StaffUiState.Error -> {
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
fun StaffOverviewCard(staffData: StaffData) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Staff Overview",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MetricItem(
                    title = "Total Staff",
                    value = "${staffData.staff.size}",
                    icon = "👥"
                )
                MetricItem(
                    title = "Teachers",
                    value = "${staffData.staff.count { it.role == com.addisababa.aischool.data.models.StaffRole.TEACHER }}",
                    icon = "👨‍🏫"
                )
                MetricItem(
                    title = "Active",
                    value = "${staffData.staff.count { it.isActive }}",
                    icon = "✅"
                )
            }
        }
    }
}

@Composable
fun StaffListCard(staffData: StaffData) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Staff Members",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            staffData.staff.forEach { staff ->
                StaffRow(staff = staff)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

@Composable
fun StaffRow(staff: com.addisababa.aischool.data.models.Staff) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(
            modifier = Modifier.size(40.dp),
            shape = MaterialTheme.shapes.circular,
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = staff.initials,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Bold
                )
            }
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(
            modifier = Modifier.weight(1f)
        ) {
            Text(
                text = staff.fullName,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = staff.role.displayName,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Surface(
            color = if (staff.isActive) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant,
            shape = MaterialTheme.shapes.small
        ) {
            Text(
                text = if (staff.isActive) "Active" else "Inactive",
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                style = MaterialTheme.typography.labelSmall
            )
        }
    }
}

@Composable
fun AssignmentsCard(staffData: StaffData) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Current Assignments",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            staffData.assignments.forEach { assignment ->
                AssignmentRow(assignment = assignment)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

@Composable
fun AssignmentRow(assignment: com.addisababa.aischool.data.models.StaffAssignment) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = assignment.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = assignment.staffName,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Column(
            horizontalAlignment = Alignment.End
        ) {
            Surface(
                color = when (assignment.status) {
                    com.addisababa.aischool.data.models.AssignmentStatus.ACTIVE -> MaterialTheme.colorScheme.primaryContainer
                    com.addisababa.aischool.data.models.AssignmentStatus.COMPLETED -> MaterialTheme.colorScheme.secondaryContainer
                    com.addisababa.aischool.data.models.AssignmentStatus.PENDING -> MaterialTheme.colorScheme.tertiaryContainer
                },
                shape = MaterialTheme.shapes.small
            ) {
                Text(
                    text = assignment.status.displayName,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall
                )
            }
            Text(
                text = assignment.dueDate,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun PerformanceCard(staffData: StaffData) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Performance Metrics",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MetricItem(
                    title = "Avg Rating",
                    value = "${staffData.performance.averageRating}/5",
                    icon = "⭐"
                )
                MetricItem(
                    title = "Tasks Completed",
                    value = "${staffData.performance.tasksCompleted}",
                    icon = "✅"
                )
                MetricItem(
                    title = "Students",
                    value = "${staffData.performance.studentsCount}",
                    icon = "👥"
                )
            }
        }
    }
}

// MARK: - UI State
sealed class StaffUiState {
    object Loading : StaffUiState()
    data class Success(val staffData: StaffData) : StaffUiState()
    data class Error(val message: String) : StaffUiState()
}