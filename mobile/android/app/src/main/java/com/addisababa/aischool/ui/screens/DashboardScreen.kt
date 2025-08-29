package com.addisababa.aischool.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun DashboardScreen(
    onNavigateToStudents: () -> Unit,
    onNavigateToAILessons: () -> Unit,
    onNavigateToAnalytics: () -> Unit,
    onNavigateToMonitoring: () -> Unit,
    onNavigateToFamilies: () -> Unit,
    onNavigateToStaff: () -> Unit,
    onNavigateToLessons: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Dashboard") }
            )
        }
    ) { paddingValues ->
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.padding(paddingValues),
            contentPadding = PaddingValues(16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(dashboardItems) { item ->
                DashboardCard(
                    item = item,
                    onClick = {
                        when (item.title) {
                            "Students" -> onNavigateToStudents()
                            "AI Lessons" -> onNavigateToAILessons()
                            "Analytics" -> onNavigateToAnalytics()
                            "Monitoring" -> onNavigateToMonitoring()
                            "Families" -> onNavigateToFamilies()
                            "Staff" -> onNavigateToStaff()
                            "Lessons" -> onNavigateToLessons()
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun DashboardCard(
    item: DashboardItem,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = item.icon,
                style = MaterialTheme.typography.displaySmall
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = item.title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(4.dp))
            
            Text(
                text = item.description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

data class DashboardItem(
    val title: String,
    val description: String,
    val icon: String
)

private val dashboardItems = listOf(
    DashboardItem(
        title = "Students",
        description = "Manage student information and progress",
        icon = "👥"
    ),
    DashboardItem(
        title = "AI Lessons",
        description = "Interactive AI-powered learning sessions",
        icon = "🤖"
    ),
    DashboardItem(
        title = "Analytics",
        description = "View learning analytics and performance",
        icon = "📊"
    ),
    DashboardItem(
        title = "Monitoring",
        description = "Monitor student behavior and engagement",
        icon = "👁️"
    ),
    DashboardItem(
        title = "Families",
        description = "Manage family connections and communication",
        icon = "🏠"
    ),
    DashboardItem(
        title = "Staff",
        description = "Manage staff members and assignments",
        icon = "👨‍🏫"
    ),
    DashboardItem(
        title = "Lessons",
        description = "Traditional lesson management",
        icon = "📚"
    )
)