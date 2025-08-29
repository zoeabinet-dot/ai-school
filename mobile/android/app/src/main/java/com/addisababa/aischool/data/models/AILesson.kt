package com.addisababa.aischool.data.models

import java.util.UUID

data class AILesson(
    val id: UUID,
    val title: String,
    val subject: String,
    val description: String,
    val difficultyLevel: DifficultyLevel,
    val estimatedDuration: Int,
    val learningObjectives: List<String>,
    val materials: List<String>,
    val isCompleted: Boolean,
    val createdAt: String
)

enum class DifficultyLevel(val displayName: String) {
    BEGINNER("Beginner"),
    INTERMEDIATE("Intermediate"),
    ADVANCED("Advanced")
}

// MARK: - Mock Data
object MockData {
    fun getMockAILessons(): List<AILesson> {
        return listOf(
            AILesson(
                id = UUID.randomUUID(),
                title = "Introduction to Algebra",
                subject = "Mathematics",
                description = "Learn the fundamentals of algebraic expressions and equations through interactive AI-powered lessons.",
                difficultyLevel = DifficultyLevel.BEGINNER,
                estimatedDuration = 45,
                learningObjectives = listOf(
                    "Understand basic algebraic expressions",
                    "Solve simple linear equations",
                    "Apply algebraic concepts to real-world problems"
                ),
                materials = listOf(
                    "Algebra Basics.pdf",
                    "Practice Problems.pdf",
                    "Interactive Quiz"
                ),
                isCompleted = false,
                createdAt = "2024-01-15"
            ),
            AILesson(
                id = UUID.randomUUID(),
                title = "Advanced Physics Concepts",
                subject = "Physics",
                description = "Explore advanced physics concepts including quantum mechanics and relativity.",
                difficultyLevel = DifficultyLevel.ADVANCED,
                estimatedDuration = 60,
                learningObjectives = listOf(
                    "Understand quantum mechanics principles",
                    "Explore relativity theory",
                    "Apply advanced physics concepts"
                ),
                materials = listOf(
                    "Quantum Physics.pdf",
                    "Relativity Theory.pdf",
                    "Virtual Lab Simulation"
                ),
                isCompleted = true,
                createdAt = "2024-01-10"
            ),
            AILesson(
                id = UUID.randomUUID(),
                title = "Creative Writing Workshop",
                subject = "English",
                description = "Develop your creative writing skills through AI-guided exercises and feedback.",
                difficultyLevel = DifficultyLevel.INTERMEDIATE,
                estimatedDuration = 30,
                learningObjectives = listOf(
                    "Improve creative writing skills",
                    "Develop unique writing style",
                    "Receive AI-powered feedback"
                ),
                materials = listOf(
                    "Writing Prompts.pdf",
                    "Style Guide.pdf",
                    "AI Writing Assistant"
                ),
                isCompleted = false,
                createdAt = "2024-01-12"
            ),
            AILesson(
                id = UUID.randomUUID(),
                title = "Ethiopian History",
                subject = "History",
                description = "Explore the rich history of Ethiopia from ancient times to modern day.",
                difficultyLevel = DifficultyLevel.INTERMEDIATE,
                estimatedDuration = 40,
                learningObjectives = listOf(
                    "Understand Ethiopian historical timeline",
                    "Learn about key historical figures",
                    "Explore cultural heritage"
                ),
                materials = listOf(
                    "Ethiopian History.pdf",
                    "Historical Timeline.pdf",
                    "Virtual Museum Tour"
                ),
                isCompleted = false,
                createdAt = "2024-01-08"
            ),
            AILesson(
                id = UUID.randomUUID(),
                title = "Computer Programming Basics",
                subject = "Computer Science",
                description = "Learn the fundamentals of computer programming with hands-on coding exercises.",
                difficultyLevel = DifficultyLevel.BEGINNER,
                estimatedDuration = 50,
                learningObjectives = listOf(
                    "Understand programming concepts",
                    "Write basic code",
                    "Debug simple programs"
                ),
                materials = listOf(
                    "Programming Guide.pdf",
                    "Code Examples.pdf",
                    "Online Code Editor"
                ),
                isCompleted = true,
                createdAt = "2024-01-05"
            )
        )
    }
}