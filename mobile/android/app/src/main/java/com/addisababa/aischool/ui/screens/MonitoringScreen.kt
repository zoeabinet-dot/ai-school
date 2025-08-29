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
import com.addisababa.aischool.data.models.MonitoringData
import com.addisababa.aischool.ui.viewmodels.MonitoringViewModel

@Composable
fun MonitoringScreen(
    modifier: Modifier = Modifier,
    viewModel: MonitoringViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.loadMonitoringData()
    }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Monitoring") },
                actions = {
                    IconButton(onClick = { /* TODO: Settings */ }) {
                        // Settings icon
                    }
                }
            )
        }
    ) { paddingValues ->
        when (uiState) {
            is MonitoringUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            is MonitoringUiState.Success -> {
                LazyColumn(
                    modifier = modifier.padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    item {
                        MonitoringStatusCard(
                            isActive = uiState.monitoringData.isActive,
                            onToggle = { viewModel.toggleMonitoring() }
                        )
                    }
                    
                    item {
                        PrivacyControlsCard(
                            monitoringData = uiState.monitoringData,
                            onPrivacySettingChanged = { setting, enabled ->
                                viewModel.updatePrivacySetting(setting, enabled)
                            }
                        )
                    }
                    
                    item {
                        RecentSessionsCard(sessions = uiState.monitoringData.recentSessions)
                    }
                    
                    item {
                        BehaviorAnalyticsCard(analytics = uiState.monitoringData.behaviorAnalytics)
                    }
                    
                    item {
                        AlertsCard(alerts = uiState.monitoringData.recentAlerts)
                    }
                }
            }
            is MonitoringUiState.Error -> {
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
fun MonitoringStatusCard(
    isActive: Boolean,
    onToggle: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "Monitoring Status",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = if (isActive) "Active" else "Inactive",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                
                Switch(
                    checked = isActive,
                    onCheckedChange = { onToggle() }
                )
            }
            
            if (isActive) {
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    StatusItem(
                        label = "Session Duration",
                        value = "45 min",
                        icon = "⏰"
                    )
                    StatusItem(
                        label = "Frames Analyzed",
                        value = "1,234",
                        icon = "👁️"
                    )
                }
            }
        }
    }
}

@Composable
fun StatusItem(
    label: String,
    value: String,
    icon: String
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = icon,
            style = MaterialTheme.typography.titleLarge
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Semibold
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun PrivacyControlsCard(
    monitoringData: MonitoringData,
    onPrivacySettingChanged: (String, Boolean) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Privacy Controls",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Face Detection",
                    style = MaterialTheme.typography.bodyMedium
                )
                Switch(
                    checked = monitoringData.faceDetectionEnabled,
                    onCheckedChange = { onPrivacySettingChanged("face_detection", it) }
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Behavior Analysis",
                    style = MaterialTheme.typography.bodyMedium
                )
                Switch(
                    checked = monitoringData.behaviorAnalysisEnabled,
                    onCheckedChange = { onPrivacySettingChanged("behavior_analysis", it) }
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Recording",
                    style = MaterialTheme.typography.bodyMedium
                )
                Switch(
                    checked = monitoringData.recordingEnabled,
                    onCheckedChange = { onPrivacySettingChanged("recording", it) }
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Alerts",
                    style = MaterialTheme.typography.bodyMedium
                )
                Switch(
                    checked = monitoringData.alertsEnabled,
                    onCheckedChange = { onPrivacySettingChanged("alerts", it) }
                )
            }
        }
    }
}

@Composable
fun RecentSessionsCard(sessions: List<MonitoringSession>) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Recent Sessions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            sessions.forEach { session ->
                SessionRow(session = session)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

@Composable
fun SessionRow(session: MonitoringSession) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = session.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = session.duration,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Column(
            horizontalAlignment = Alignment.End
        ) {
            Surface(
                color = when (session.status) {
                    SessionStatus.ACTIVE -> MaterialTheme.colorScheme.primaryContainer
                    SessionStatus.COMPLETED -> MaterialTheme.colorScheme.secondaryContainer
                    SessionStatus.INTERRUPTED -> MaterialTheme.colorScheme.tertiaryContainer
                },
                shape = MaterialTheme.shapes.small
            ) {
                Text(
                    text = session.status.displayName,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall
                )
            }
            Text(
                text = session.date,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun BehaviorAnalyticsCard(analytics: BehaviorAnalytics) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Behavior Analytics",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MetricItem(
                    title = "Attention Score",
                    value = "${analytics.attentionScore}%",
                    icon = "👁️"
                )
                MetricItem(
                    title = "Engagement",
                    value = "${analytics.engagementScore}%",
                    icon = "🧠"
                )
                MetricItem(
                    title = "Focus Time",
                    value = "${analytics.focusTime}min",
                    icon = "⏰"
                )
                MetricItem(
                    title = "Distractions",
                    value = "${analytics.distractions}",
                    icon = "⚠️"
                )
            }
        }
    }
}

@Composable
fun AlertsCard(alerts: List<MonitoringAlert>) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Recent Alerts",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            alerts.forEach { alert ->
                AlertRow(alert = alert)
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

@Composable
fun AlertRow(alert: MonitoringAlert) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(
            modifier = Modifier.size(40.dp),
            shape = MaterialTheme.shapes.circular,
            color = alert.severity.color
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = alert.icon,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
        
        Spacer(modifier = Modifier.width(12.dp))
        
        Column(
            modifier = Modifier.weight(1f)
        ) {
            Text(
                text = alert.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = alert.description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        
        Text(
            text = alert.timeAgo,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// MARK: - UI State
sealed class MonitoringUiState {
    object Loading : MonitoringUiState()
    data class Success(val monitoringData: MonitoringData) : MonitoringUiState()
    data class Error(val message: String) : MonitoringUiState()
}