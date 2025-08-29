package com.addisababa.aischool

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.addisababa.aischool.ui.screens.DashboardScreen
import com.addisababa.aischool.ui.screens.LoginScreen
import com.addisababa.aischool.ui.screens.StudentListScreen
import com.addisababa.aischool.ui.screens.AILessonScreen
import com.addisababa.aischool.ui.screens.AnalyticsScreen
import com.addisababa.aischool.ui.screens.MonitoringScreen
import com.addisababa.aischool.ui.screens.FamilyScreen
import com.addisababa.aischool.ui.screens.StaffScreen
import com.addisababa.aischool.ui.screens.LessonsScreen
import com.addisababa.aischool.ui.theme.AddisAbabaAISchoolTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            AddisAbabaAISchoolTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AISchoolApp()
                }
            }
        }
    }
}

@Composable
fun AISchoolApp() {
    val navController = rememberNavController()
    
    Scaffold { paddingValues ->
        NavHost(
            navController = navController,
            startDestination = "login",
            modifier = Modifier.padding(paddingValues)
        ) {
            composable("login") {
                LoginScreen(
                    onLoginSuccess = {
                        navController.navigate("dashboard") {
                            popUpTo("login") { inclusive = true }
                        }
                    }
                )
            }
            
            composable("dashboard") {
                DashboardScreen(
                    onNavigateToStudents = { navController.navigate("students") },
                    onNavigateToAILessons = { navController.navigate("ai_lessons") },
                    onNavigateToAnalytics = { navController.navigate("analytics") },
                    onNavigateToMonitoring = { navController.navigate("monitoring") },
                    onNavigateToFamilies = { navController.navigate("families") },
                    onNavigateToStaff = { navController.navigate("staff") },
                    onNavigateToLessons = { navController.navigate("lessons") }
                )
            }
            
            composable("students") {
                StudentListScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onStudentSelected = { studentId ->
                        // Navigate to student detail
                    }
                )
            }
            
            composable("ai_lessons") {
                AILessonScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onLessonSelected = { lessonId ->
                        // Navigate to lesson detail
                    }
                )
            }
            
            composable("analytics") {
                AnalyticsScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            
            composable("monitoring") {
                MonitoringScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            
            composable("families") {
                FamilyScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onFamilySelected = { familyId ->
                        // Navigate to family detail
                    }
                )
            }
            
            composable("staff") {
                StaffScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onStaffSelected = { staffId ->
                        // Navigate to staff detail
                    }
                )
            }
            
            composable("lessons") {
                LessonsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onLessonSelected = { lessonId ->
                        // Navigate to lesson detail
                    }
                )
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    AddisAbabaAISchoolTheme {
        Text("Addis Ababa AI School")
    }
}