package com.addisababa.aischool.data.models

import java.util.*

// MARK: - Personalized Learning Models

data class PersonalizedLearningPath(
    val id: String,
    val subject: String,
    val currentLevel: String,
    val targetLevel: String,
    val learningSteps: List<LearningStep>,
    val estimatedDuration: Int, // minutes
    val difficultyProgression: DifficultyProgression,
    val learningStyle: LearningStyle,
    val adaptiveElements: List<AdaptiveElement>,
    val createdAt: Date = Date(),
    val lastUpdated: Date = Date()
)

data class LearningStep(
    val id: String,
    val title: String,
    val description: String,
    val duration: Int, // minutes
    val difficulty: DifficultyLevel,
    val resources: List<LearningResource>,
    val prerequisites: List<String> = emptyList(),
    val learningObjectives: List<String> = emptyList(),
    val assessmentCriteria: List<String> = emptyList()
)

data class LearningResource(
    val id: String,
    val type: ResourceType,
    val title: String,
    val url: String?,
    val content: String?,
    val duration: Int, // minutes
    val difficulty: DifficultyLevel,
    val tags: List<String> = emptyList()
)

data class AdaptiveElement(
    val id: String,
    val type: AdaptiveType,
    val trigger: AdaptiveTrigger,
    val action: AdaptiveAction,
    val conditions: List<AdaptiveCondition>
)

data class AdaptedLessonContent(
    val id: String,
    val originalLessonId: String,
    val studentId: String,
    val adaptedContent: String,
    val difficultyAdjustment: DifficultyAdjustment,
    val formatChanges: List<FormatChange>,
    val additionalResources: List<LearningResource>,
    val estimatedCompletionTime: Int, // minutes
    val confidence: Float // 0.0 to 1.0
)

data class RecommendedActivity(
    val id: String,
    val title: String,
    val description: String,
    val type: ActivityType,
    val subject: String,
    val difficulty: DifficultyLevel,
    val estimatedDuration: Int, // minutes
    val priority: Priority,
    val reasoning: String,
    val expectedOutcome: String
)

// MARK: - Predictive Analytics Models

data class PerformancePrediction(
    val id: String,
    val studentId: String,
    val subject: String,
    val assessmentType: AssessmentType,
    val predictedScore: Float, // 0.0 to 100.0
    val confidence: Float, // 0.0 to 1.0
    val timeHorizon: TimeHorizon,
    val factors: List<PredictionFactor>,
    val recommendations: List<String>,
    val riskLevel: RiskLevel,
    val predictedDate: Date
)

data class PredictionFactor(
    val factor: String,
    val impact: Float, // -1.0 to 1.0
    val description: String,
    val confidence: Float
)

data class AtRiskStudent(
    val studentId: String,
    val riskFactors: List<RiskFactor>,
    val riskScore: Float, // 0.0 to 1.0
    val subjects: List<String>,
    val earlyWarningSigns: List<String>,
    val recommendedInterventions: List<String>,
    val urgency: Urgency
)

data class RiskFactor(
    val type: RiskType,
    val severity: Severity,
    val description: String,
    val evidence: String,
    val confidence: Float
)

data class OptimalStudySchedule(
    val id: String,
    val studentId: String,
    val subjects: List<SubjectSchedule>,
    val totalStudyTime: Int, // minutes per day
    val breaks: List<Break>,
    val optimalTimes: List<OptimalTimeSlot>,
    val retentionOptimization: RetentionStrategy,
    val cognitiveLoadManagement: CognitiveLoadStrategy
)

data class SubjectSchedule(
    val subject: String,
    val dailyTime: Int, // minutes
    val frequency: StudyFrequency,
    val optimalTimeOfDay: TimeOfDay,
    val difficulty: DifficultyLevel
)

data class AcademicTrajectory(
    val studentId: String,
    val currentGrade: String,
    val predictedGrades: List<PredictedGrade>,
    val collegeReadiness: CollegeReadiness,
    val careerPathways: List<CareerPathway>,
    val skillGaps: List<SkillGap>,
    val recommendations: List<String>,
    val confidence: Float
)

data class PredictedGrade(
    val year: Int,
    val subject: String,
    val predictedGrade: String,
    val confidence: Float,
    val factors: List<String>
)

// MARK: - Natural Language Generation Models

data class GeneratedExplanation(
    val id: String,
    val concept: String,
    val explanation: String,
    val complexity: Complexity,
    val examples: List<String>,
    val analogies: List<String>,
    val visualSuggestions: List<String>,
    val followUpQuestions: List<String>,
    val relatedConcepts: List<String>,
    val confidence: Float
)

data class GeneratedQuestion(
    val id: String,
    val question: String,
    val type: QuestionType,
    val difficulty: DifficultyLevel,
    val subject: String,
    val topic: String,
    val options: List<String>?, // For multiple choice
    val correctAnswer: String,
    val explanation: String,
    val hints: List<String>,
    val tags: List<String>
)

data class GeneratedFeedback(
    val id: String,
    val assignmentId: String,
    val studentId: String,
    val feedback: String,
    val tone: FeedbackTone,
    val specificComments: List<SpecificComment>,
    val encouragement: String,
    val nextSteps: List<String>,
    val resources: List<LearningResource>,
    val confidence: Float
)

data class SpecificComment(
    val aspect: String,
    val comment: String,
    val suggestion: String,
    val positive: Boolean
)

data class LearningSummary(
    val id: String,
    val topic: String,
    val summary: String,
    val keyPoints: List<String>,
    val examples: List<String>,
    val practiceQuestions: List<GeneratedQuestion>,
    val visualElements: List<String>,
    val relatedTopics: List<String>,
    val difficulty: DifficultyLevel,
    val estimatedReadingTime: Int // minutes
)

// MARK: - Emotional Intelligence Models

data class EmotionalAnalysis(
    val id: String,
    val studentId: String,
    val sessionId: String,
    val timestamp: Date,
    val primaryEmotion: Emotion,
    val emotionIntensity: Float, // 0.0 to 1.0
    val secondaryEmotions: List<Emotion>,
    val confidence: Float,
    val facialExpressions: List<FacialExpression>,
    val behavioralPatterns: List<BehavioralPattern>,
    val learningImpact: LearningImpact,
    val recommendations: List<String>
)

data class Emotion(
    val type: EmotionType,
    val intensity: Float, // 0.0 to 1.0
    val duration: Int, // seconds
    val context: String,
    val confidence: Float
)

data class FacialExpression(
    val type: ExpressionType,
    val confidence: Float,
    val timestamp: Date,
    val coordinates: FacialCoordinates?
)

data class FacialCoordinates(
    val x: Float,
    val y: Float,
    val width: Float,
    val height: Float
)

data class BehavioralPattern(
    val type: BehaviorType,
    val frequency: Int,
    val duration: Int, // seconds
    val context: String,
    val significance: Significance
)

data class FrustrationDetection(
    val studentId: String,
    val isFrustrated: Boolean,
    val frustrationLevel: FrustrationLevel,
    val triggers: List<String>,
    val duration: Int, // minutes
    val impactOnLearning: LearningImpact,
    val recommendedInterventions: List<String>,
    val urgency: Urgency
)

data class EmotionalSupport(
    val id: String,
    val studentId: String,
    val emotionalState: EmotionalState,
    val supportMessage: String,
    val supportType: SupportType,
    val resources: List<SupportResource>,
    val followUpActions: List<String>,
    val expectedOutcome: String,
    val confidence: Float
)

data class SupportResource(
    val type: ResourceType,
    val title: String,
    val content: String,
    val duration: Int, // minutes
    val effectiveness: Float // 0.0 to 1.0
)

data class EmotionalResponsePrediction(
    val studentId: String,
    val challenge: LearningChallenge,
    val predictedResponse: EmotionalResponse,
    val confidence: Float,
    val riskFactors: List<String>,
    val preventiveMeasures: List<String>,
    val supportStrategies: List<String>
)

// MARK: - Advanced AI Feature Models

data class LearningOptimization(
    val studentId: String,
    val sessionId: String,
    val optimizations: List<Optimization>,
    val performanceImpact: Float, // 0.0 to 1.0
    val recommendations: List<String>,
    val nextSteps: List<String>
)

data class Optimization(
    val type: OptimizationType,
    val description: String,
    val impact: Float, // 0.0 to 1.0
    val implementation: String,
    val expectedOutcome: String
)

data class MultiModalContent(
    val id: String,
    val topic: String,
    val textContent: String?,
    val visualContent: List<VisualElement>?,
    val audioContent: List<AudioElement>?,
    val interactiveElements: List<InteractiveElement>?,
    val learningObjectives: List<String>,
    val targetAudience: StudentProfile,
    val estimatedDuration: Int, // minutes
    val difficulty: DifficultyLevel
)

data class VisualElement(
    val type: VisualType,
    val content: String, // URL or base64 data
    val description: String,
    val altText: String,
    val size: ContentSize
)

data class AudioElement(
    val type: AudioType,
    val content: String, // URL or base64 data
    val duration: Int, // seconds
    val transcript: String?,
    val description: String
)

data class InteractiveElement(
    val type: InteractiveType,
    val content: String,
    val description: String,
    val expectedInteraction: String,
    val feedback: String
)

data class CollaborativeLearningRecommendation(
    val id: String,
    val studentId: String,
    val subject: String,
    val recommendedGroups: List<StudyGroup>,
    val peerMentors: List<PeerMentor>,
    val collaborativeActivities: List<CollaborativeActivity>,
    val expectedBenefits: List<String>,
    val implementation: String
)

data class StudyGroup(
    val id: String,
    val members: List<String>, // student IDs
    val subject: String,
    val meetingTime: String,
    val duration: Int, // minutes
    val focus: String,
    val compatibility: Float // 0.0 to 1.0
)

data class PeerMentor(
    val studentId: String,
    val strengths: List<String>,
    val subjects: List<String>,
    val availability: String,
    val mentoringStyle: MentoringStyle,
    val compatibility: Float // 0.0 to 1.0
)

data class CollaborativeActivity(
    val id: String,
    val title: String,
    val description: String,
    val type: ActivityType,
    val participants: Int,
    val duration: Int, // minutes
    val learningObjectives: List<String>
)

data class AdaptiveAssessment(
    val id: String,
    val subject: String,
    val questions: List<AdaptiveQuestion>,
    val learningObjectives: List<String>,
    val studentProfile: StudentProfile,
    val estimatedDuration: Int, // minutes
    val difficulty: DifficultyLevel,
    val adaptiveAlgorithm: AdaptiveAlgorithm
)

data class AdaptiveQuestion(
    val id: String,
    val question: GeneratedQuestion,
    val difficulty: DifficultyLevel,
    val nextQuestionLogic: NextQuestionLogic,
    val timeLimit: Int? // seconds
)

// MARK: - Enums and Constants

enum class LearningStyle {
    VISUAL, AUDITORY, KINESTHETIC, READING_WRITING, MIXED
}

enum class DifficultyProgression {
    GRADUAL, STEPPED, EXPONENTIAL, CUSTOM
}

enum class DifficultyLevel {
    VERY_EASY, EASY, MEDIUM, HARD, VERY_HARD, EXPERT
}

enum class ResourceType {
    VIDEO, AUDIO, TEXT, IMAGE, INTERACTIVE, QUIZ, EXERCISE, GAME
}

enum class AdaptiveType {
    DIFFICULTY, PACE, CONTENT, FORMAT, RESOURCES
}

enum class AdaptiveTrigger {
    PERFORMANCE, TIME, ENGAGEMENT, FRUSTRATION, SUCCESS
}

enum class AdaptiveAction {
    INCREASE_DIFFICULTY, DECREASE_DIFFICULTY, CHANGE_FORMAT, ADD_RESOURCES, PAUSE
}

enum class ActivityType {
    QUIZ, EXERCISE, PROJECT, DISCUSSION, PRESENTATION, GAME, SIMULATION
}

enum class Priority {
    LOW, MEDIUM, HIGH, URGENT
}

enum class AssessmentType {
    QUIZ, TEST, EXAM, PROJECT, PRESENTATION, ASSIGNMENT
}

enum class TimeHorizon {
    SHORT_TERM, MEDIUM_TERM, LONG_TERM
}

enum class RiskLevel {
    LOW, MEDIUM, HIGH, CRITICAL
}

enum class Urgency {
    LOW, MEDIUM, HIGH, IMMEDIATE
}

enum class RiskType {
    ACADEMIC, BEHAVIORAL, ATTENDANCE, SOCIAL, EMOTIONAL
}

enum class Severity {
    MILD, MODERATE, SEVERE, CRITICAL
}

enum class StudyFrequency {
    DAILY, EVERY_OTHER_DAY, WEEKLY, BIWEEKLY, MONTHLY
}

enum class TimeOfDay {
    MORNING, AFTERNOON, EVENING, NIGHT
}

enum class Complexity {
    VERY_SIMPLE, SIMPLE, MODERATE, COMPLEX, VERY_COMPLEX
}

enum class QuestionType {
    MULTIPLE_CHOICE, TRUE_FALSE, SHORT_ANSWER, ESSAY, MATCHING, FILL_BLANK
}

enum class FeedbackTone {
    ENCOURAGING, CONSTRUCTIVE, NEUTRAL, MOTIVATIONAL, SUPPORTIVE
}

enum class EmotionType {
    HAPPY, SAD, ANGRY, FRUSTRATED, EXCITED, BORED, CONFUSED, CONFIDENT, ANXIOUS, CALM
}

enum class ExpressionType {
    SMILE, FROWN, RAISED_EYEBROWS, SQUINT, OPEN_MOUTH, TIGHT_LIPS
}

enum class BehaviorType {
    FIDGETING, LOOKING_AWAY, SIGHING, TAPPING, SCRATCHING, YAWNING
}

enum class Significance {
    LOW, MEDIUM, HIGH, CRITICAL
}

enum class FrustrationLevel {
    NONE, MILD, MODERATE, HIGH, EXTREME
}

enum class LearningImpact {
    POSITIVE, NEUTRAL, NEGATIVE, SEVERE
}

enum class EmotionalState {
    CALM, EXCITED, FRUSTRATED, CONFUSED, CONFIDENT, ANXIOUS, BORED, ENGAGED
}

enum class SupportType {
    ENCOURAGEMENT, GUIDANCE, BREAK, RESOURCE, INTERVENTION, REFERRAL
}

enum class ContentSize {
    SMALL, MEDIUM, LARGE, FULL_SCREEN
}

enum class VisualType {
    DIAGRAM, CHART, GRAPH, ILLUSTRATION, PHOTO, VIDEO_FRAME
}

enum class AudioType {
    EXPLANATION, MUSIC, SOUND_EFFECT, AMBIENT, INSTRUCTION
}

enum class InteractiveType {
    QUIZ, DRAG_DROP, SIMULATION, GAME, EXERCISE, EXPLORATION
}

enum class MentoringStyle {
    GUIDED, COLLABORATIVE, CHALLENGING, SUPPORTIVE, STRUCTURED
}

enum class AdaptiveAlgorithm {
    ITEM_RESPONSE_THEORY, BAYESIAN_NETWORK, MACHINE_LEARNING, HYBRID
}

enum class NextQuestionLogic {
    INCREASE_DIFFICULTY, DECREASE_DIFFICULTY, MAINTAIN_LEVEL, RANDOM, ADAPTIVE
}