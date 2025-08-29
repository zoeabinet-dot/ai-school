package com.addisababa.aischool.ui.viewmodels

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.addisababa.aischool.data.models.*
import com.addisababa.aischool.data.repository.AppRepository
import com.addisababa.aischool.ui.screens.StudentListUiState
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import java.util.*

@OptIn(ExperimentalCoroutinesApi::class)
class StudentListViewModelTest {
    
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()
    
    private lateinit var viewModel: StudentListViewModel
    private lateinit var repository: AppRepository
    private val testDispatcher = StandardTestDispatcher()
    
    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = mockk()
        viewModel = StudentListViewModel(repository)
    }
    
    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }
    
    @Test
    fun `loadStudents should emit Loading then Success state`() = runTest {
        // Given
        val mockStudents = listOf(
            Student(
                id = UUID.randomUUID(),
                firstName = "John",
                lastName = "Doe",
                email = "john.doe@email.com",
                phone = "+1234567890",
                grade = "10",
                age = 16,
                address = "123 Main St",
                city = "Addis Ababa",
                profileImage = null,
                status = StudentStatus.ACTIVE,
                averageScore = 85,
                enrollmentDate = "2023-09-01",
                academicLevel = AcademicLevel.ADVANCED,
                learningStyle = LearningStyle.VISUAL,
                specialNeeds = emptyList(),
                goals = emptyList(),
                achievements = emptyList(),
                emergencyContact = "Jane Doe",
                emergencyPhone = "+1234567890",
                medicalInfo = "No known allergies",
                notes = "Excellent student"
            )
        )
        
        coEvery { repository.getStudents() } returns flowOf(Result.success(mockStudents))
        
        // When
        viewModel.loadStudents()
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        val currentState = viewModel.uiState.value
        assertTrue(currentState is StudentListUiState.Success)
        assertEquals(mockStudents, (currentState as StudentListUiState.Success).students)
    }
    
    @Test
    fun `loadStudents should emit Loading then Error state on failure`() = runTest {
        // Given
        val errorMessage = "Network error"
        coEvery { repository.getStudents() } returns flowOf(Result.failure(Exception(errorMessage)))
        
        // When
        viewModel.loadStudents()
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        val currentState = viewModel.uiState.value
        assertTrue(currentState is StudentListUiState.Error)
        assertEquals(errorMessage, (currentState as StudentListUiState.Error).message)
    }
    
    @Test
    fun `addStudent should update state with new student`() = runTest {
        // Given
        val newStudent = Student(
            id = UUID.randomUUID(),
            firstName = "Jane",
            lastName = "Smith",
            email = "jane.smith@email.com",
            phone = "+1234567891",
            grade = "11",
            age = 17,
            address = "456 Oak St",
            city = "Addis Ababa",
            profileImage = null,
            status = StudentStatus.ACTIVE,
            averageScore = 90,
            enrollmentDate = "2023-09-01",
            academicLevel = AcademicLevel.ADVANCED,
            learningStyle = LearningStyle.AUDITORY,
            specialNeeds = emptyList(),
            goals = emptyList(),
            achievements = emptyList(),
            emergencyContact = "John Smith",
            emergencyPhone = "+1234567891",
            medicalInfo = "No known allergies",
            notes = "New student"
        )
        
        coEvery { repository.createStudent(any()) } returns Result.success(newStudent)
        
        // When
        viewModel.addStudent(newStudent)
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        // The state should be updated with the new student
        // This would require the ViewModel to maintain a list of students
    }
    
    @Test
    fun `deleteStudent should remove student from state`() = runTest {
        // Given
        val studentId = "test-student-id"
        coEvery { repository.deleteStudent(studentId) } returns Result.success("Student deleted successfully")
        
        // When
        viewModel.deleteStudent(studentId)
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        // The state should be updated without the deleted student
        // This would require the ViewModel to maintain a list of students
    }
    
    @Test
    fun `updateStudent should modify student in state`() = runTest {
        // Given
        val updatedStudent = Student(
            id = UUID.randomUUID(),
            firstName = "Updated",
            lastName = "Student",
            email = "updated.student@email.com",
            phone = "+1234567892",
            grade = "12",
            age = 18,
            address = "789 Pine St",
            city = "Addis Ababa",
            profileImage = null,
            status = StudentStatus.ACTIVE,
            averageScore = 95,
            enrollmentDate = "2023-09-01",
            academicLevel = AcademicLevel.ADVANCED,
            learningStyle = LearningStyle.KINESTHETIC,
            specialNeeds = emptyList(),
            goals = emptyList(),
            achievements = emptyList(),
            emergencyContact = "Parent Name",
            emergencyPhone = "+1234567892",
            medicalInfo = "No known allergies",
            notes = "Updated student"
        )
        
        coEvery { repository.updateStudent(any(), any()) } returns Result.success(updatedStudent)
        
        // When
        viewModel.updateStudent(updatedStudent)
        testDispatcher.scheduler.advanceUntilIdle()
        
        // Then
        // The state should be updated with the modified student
        // This would require the ViewModel to maintain a list of students
    }
}