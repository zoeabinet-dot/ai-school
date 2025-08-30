package com.addisababa.aischool.ai

import com.addisababa.aischool.data.models.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.*

/**
 * Emotional Intelligence Service
 * Handles student emotion recognition, frustration detection, and emotional support generation
 */
interface EmotionalIntelligenceService {
    
    /**
     * Analyze student emotions during learning sessions
     */
    suspend fun analyzeStudentEmotions(
        sessionData: LearningSessionData,
        facialExpressions: List<FacialExpression>,
        behavioralPatterns: List<BehavioralPattern>
    ): EmotionalAnalysis
    
    /**
     * Detect learning frustration and provide support
     */
    suspend fun detectLearningFrustration(
        studentId: String,
        recentInteractions: List<InteractionData>,
        performanceMetrics: PerformanceMetrics
    ): FrustrationDetection
    
    /**
     * Generate emotional support responses
     */
    suspend fun generateEmotionalSupport(
        studentId: String,
        emotionalState: EmotionalState,
        context: String,
        previousSupport: List<SupportMessage>
    ): EmotionalSupport
    
    /**
     * Predict emotional responses to learning challenges
     */
    suspend fun predictEmotionalResponse(
        studentId: String,
        upcomingChallenge: LearningChallenge,
        historicalResponses: List<EmotionalResponse>
    ): EmotionalResponsePrediction
    
    /**
     * Monitor emotional well-being over time
     */
    suspend fun monitorEmotionalWellbeing(
        studentId: String,
        timeRange: TimeRange
    ): EmotionalWellbeingReport
    
    /**
     * Generate personalized emotional learning strategies
     */
    suspend fun generateEmotionalLearningStrategies(
        studentId: String,
        emotionalProfile: EmotionalProfile,
        learningGoals: List<String>
    ): List<EmotionalLearningStrategy>
}

/**
 * Implementation of Emotional Intelligence Service
 */
class EmotionalIntelligenceServiceImpl(
    private val emotionRecognitionService: EmotionRecognitionService,
    private val behavioralAnalysisService: BehavioralAnalysisService,
    private val supportGenerationService: SupportGenerationService,
    private val mlService: MLService
) : EmotionalIntelligenceService {
    
    override suspend fun analyzeStudentEmotions(
        sessionData: LearningSessionData,
        facialExpressions: List<FacialExpression>,
        behavioralPatterns: List<BehavioralPattern>
    ): EmotionalAnalysis {
        return try {
            // Step 1: Analyze facial expressions
            val facialAnalysis = emotionRecognitionService.analyzeFacialExpressions(facialExpressions)
            
            // Step 2: Analyze behavioral patterns
            val behavioralAnalysis = behavioralAnalysisService.analyzeBehavioralPatterns(behavioralPatterns)
            
            // Step 3: Combine facial and behavioral analysis
            val combinedAnalysis = combineEmotionalAnalysis(facialAnalysis, behavioralAnalysis)
            
            // Step 4: Determine primary and secondary emotions
            val primaryEmotion = determinePrimaryEmotion(combinedAnalysis)
            val secondaryEmotions = determineSecondaryEmotions(combinedAnalysis, primaryEmotion)
            
            // Step 5: Calculate emotion intensity and confidence
            val emotionIntensity = calculateEmotionIntensity(combinedAnalysis)
            val confidence = calculateAnalysisConfidence(facialAnalysis, behavioralAnalysis)
            
            // Step 6: Assess learning impact
            val learningImpact = assessLearningImpact(primaryEmotion, emotionIntensity, sessionData)
            
            // Step 7: Generate recommendations
            val recommendations = generateEmotionalRecommendations(
                primaryEmotion, emotionIntensity, learningImpact
            )
            
            EmotionalAnalysis(
                id = "emotion_${sessionData.studentId}_${System.currentTimeMillis()}",
                studentId = sessionData.studentId,
                sessionId = sessionData.sessionId,
                timestamp = Date(),
                primaryEmotion = primaryEmotion,
                emotionIntensity = emotionIntensity,
                secondaryEmotions = secondaryEmotions,
                confidence = confidence,
                facialExpressions = facialExpressions,
                behavioralPatterns = behavioralPatterns,
                learningImpact = learningImpact,
                recommendations = recommendations
            )
        } catch (e: Exception) {
            // Fallback analysis
            generateFallbackEmotionalAnalysis(sessionData)
        }
    }
    
    override suspend fun detectLearningFrustration(
        studentId: String,
        recentInteractions: List<InteractionData>,
        performanceMetrics: PerformanceMetrics
    ): FrustrationDetection {
        return try {
            // Step 1: Analyze interaction patterns
            val interactionAnalysis = analyzeInteractionPatterns(recentInteractions)
            
            // Step 2: Analyze performance trends
            val performanceAnalysis = analyzePerformanceTrends(performanceMetrics)
            
            // Step 3: Detect frustration indicators
            val frustrationIndicators = detectFrustrationIndicators(
                interactionAnalysis, performanceAnalysis
            )
            
            // Step 4: Calculate frustration level
            val frustrationLevel = calculateFrustrationLevel(frustrationIndicators)
            
            // Step 5: Identify triggers
            val triggers = identifyFrustrationTriggers(
                interactionAnalysis, performanceAnalysis, frustrationIndicators
            )
            
            // Step 6: Assess impact on learning
            val learningImpact = assessFrustrationImpact(frustrationLevel, performanceMetrics)
            
            // Step 7: Generate intervention recommendations
            val interventions = generateFrustrationInterventions(
                frustrationLevel, triggers, learningImpact
            )
            
            // Step 8: Determine urgency
            val urgency = calculateFrustrationUrgency(frustrationLevel, learningImpact)
            
            FrustrationDetection(
                studentId = studentId,
                isFrustrated = frustrationLevel != FrustrationLevel.NONE,
                frustrationLevel = frustrationLevel,
                triggers = triggers,
                duration = calculateFrustrationDuration(recentInteractions),
                impactOnLearning = learningImpact,
                recommendedInterventions = interventions,
                urgency = urgency
            )
        } catch (e: Exception) {
            // Fallback detection
            generateFallbackFrustrationDetection(studentId)
        }
    }
    
    override suspend fun generateEmotionalSupport(
        studentId: String,
        emotionalState: EmotionalState,
        context: String,
        previousSupport: List<SupportMessage>
    ): EmotionalSupport {
        return try {
            // Step 1: Analyze emotional state
            val emotionalAnalysis = analyzeEmotionalState(emotionalState, context)
            
            // Step 2: Generate appropriate support message
            val supportMessage = generateSupportMessage(emotionalState, context, emotionalAnalysis)
            
            // Step 3: Determine support type
            val supportType = determineSupportType(emotionalState, emotionalAnalysis)
            
            // Step 4: Generate support resources
            val supportResources = generateSupportResources(
                emotionalState, supportType, studentId
            )
            
            // Step 5: Plan follow-up actions
            val followUpActions = planFollowUpActions(
                emotionalState, supportType, previousSupport
            )
            
            // Step 6: Predict expected outcome
            val expectedOutcome = predictSupportOutcome(
                emotionalState, supportType, supportResources
            )
            
            // Step 7: Calculate confidence
            val confidence = calculateSupportConfidence(
                emotionalState, supportType, previousSupport
            )
            
            EmotionalSupport(
                id = "support_${studentId}_${System.currentTimeMillis()}",
                studentId = studentId,
                emotionalState = emotionalState,
                supportMessage = supportMessage,
                supportType = supportType,
                resources = supportResources,
                followUpActions = followUpActions,
                expectedOutcome = expectedOutcome,
                confidence = confidence
            )
        } catch (e: Exception) {
            // Fallback support
            generateFallbackEmotionalSupport(studentId, emotionalState)
        }
    }
    
    override suspend fun predictEmotionalResponse(
        studentId: String,
        upcomingChallenge: LearningChallenge,
        historicalResponses: List<EmotionalResponse>
    ): EmotionalResponsePrediction {
        return try {
            // Step 1: Analyze historical emotional responses
            val responsePatterns = analyzeResponsePatterns(historicalResponses)
            
            // Step 2: Assess challenge characteristics
            val challengeAssessment = assessChallengeCharacteristics(upcomingChallenge)
            
            // Step 3: Predict emotional response using ML
            val predictedResponse = mlService.predictEmotionalResponse(
                responsePatterns, challengeAssessment
            )
            
            // Step 4: Identify risk factors
            val riskFactors = identifyEmotionalRiskFactors(
                responsePatterns, challengeAssessment, predictedResponse
            )
            
            // Step 5: Generate preventive measures
            val preventiveMeasures = generatePreventiveMeasures(
                riskFactors, predictedResponse
            )
            
            // Step 6: Develop support strategies
            val supportStrategies = developSupportStrategies(
                predictedResponse, riskFactors, preventiveMeasures
            )
            
            // Step 7: Calculate prediction confidence
            val confidence = calculatePredictionConfidence(
                responsePatterns, challengeAssessment
            )
            
            EmotionalResponsePrediction(
                studentId = studentId,
                challenge = upcomingChallenge,
                predictedResponse = predictedResponse,
                confidence = confidence,
                riskFactors = riskFactors,
                preventiveMeasures = preventiveMeasures,
                supportStrategies = supportStrategies
            )
        } catch (e: Exception) {
            // Fallback prediction
            generateFallbackEmotionalResponsePrediction(studentId, upcomingChallenge)
        }
    }
    
    override suspend fun monitorEmotionalWellbeing(
        studentId: String,
        timeRange: TimeRange
    ): EmotionalWellbeingReport {
        return try {
            // Step 1: Gather emotional data over time
            val emotionalData = gatherEmotionalData(studentId, timeRange)
            
            // Step 2: Analyze emotional trends
            val emotionalTrends = analyzeEmotionalTrends(emotionalData)
            
            // Step 3: Identify patterns and cycles
            val emotionalPatterns = identifyEmotionalPatterns(emotionalData)
            
            // Step 4: Assess overall wellbeing
            val wellbeingScore = calculateWellbeingScore(emotionalTrends, emotionalPatterns)
            
            // Step 5: Generate insights
            val insights = generateWellbeingInsights(emotionalTrends, emotionalPatterns)
            
            // Step 6: Recommend improvements
            val recommendations = recommendWellbeingImprovements(
                wellbeingScore, insights, emotionalPatterns
            )
            
            EmotionalWellbeingReport(
                id = "wellbeing_${studentId}_${System.currentTimeMillis()}",
                studentId = studentId,
                timeRange = timeRange,
                wellbeingScore = wellbeingScore,
                emotionalTrends = emotionalTrends,
                emotionalPatterns = emotionalPatterns,
                insights = insights,
                recommendations = recommendations,
                confidence = calculateWellbeingConfidence(emotionalData)
            )
        } catch (e: Exception) {
            // Fallback report
            generateFallbackWellbeingReport(studentId, timeRange)
        }
    }
    
    override suspend fun generateEmotionalLearningStrategies(
        studentId: String,
        emotionalProfile: EmotionalProfile,
        learningGoals: List<String>
    ): List<EmotionalLearningStrategy> {
        return try {
            val strategies = mutableListOf<EmotionalLearningStrategy>()
            
            // Step 1: Analyze emotional profile
            val profileAnalysis = analyzeEmotionalProfile(emotionalProfile)
            
            // Step 2: Generate strategies for each learning goal
            learningGoals.forEach { goal ->
                val goalStrategies = generateGoalSpecificStrategies(
                    goal, emotionalProfile, profileAnalysis
                )
                strategies.addAll(goalStrategies)
            }
            
            // Step 3: Add general emotional learning strategies
            val generalStrategies = generateGeneralEmotionalStrategies(emotionalProfile)
            strategies.addAll(generalStrategies)
            
            // Step 4: Prioritize strategies
            val prioritizedStrategies = prioritizeStrategies(strategies, emotionalProfile)
            
            // Step 5: Add implementation details
            prioritizedStrategies.map { strategy ->
                enrichStrategy(strategy, emotionalProfile)
            }
        } catch (e: Exception) {
            // Fallback strategies
            generateFallbackEmotionalStrategies(studentId, learningGoals)
        }
    }
    
    // MARK: - Private Helper Methods
    
    private suspend fun combineEmotionalAnalysis(
        facialAnalysis: FacialAnalysis,
        behavioralAnalysis: BehavioralAnalysis
    ): CombinedEmotionalAnalysis {
        return CombinedEmotionalAnalysis(
            facialConfidence = facialAnalysis.confidence,
            behavioralConfidence = behavioralAnalysis.confidence,
            combinedConfidence = (facialAnalysis.confidence + behavioralAnalysis.confidence) / 2.0f,
            emotions = facialAnalysis.emotions + behavioralAnalysis.emotions,
            patterns = behavioralAnalysis.patterns
        )
    }
    
    private suspend fun determinePrimaryEmotion(
        analysis: CombinedEmotionalAnalysis
    ): Emotion {
        return analysis.emotions.maxByOrNull { it.intensity } ?: Emotion(
            type = EmotionType.CALM,
            intensity = 0.5f,
            duration = 0,
            context = "default",
            confidence = 0.5f
        )
    }
    
    private suspend fun determineSecondaryEmotions(
        analysis: CombinedEmotionalAnalysis,
        primary: Emotion
    ): List<Emotion> {
        return analysis.emotions
            .filter { it.type != primary.type }
            .sortedByDescending { it.intensity }
            .take(2)
    }
    
    private suspend fun calculateEmotionIntensity(
        analysis: CombinedEmotionalAnalysis
    ): Float {
        val avgIntensity = analysis.emotions.map { it.intensity }.average().toFloat()
        return (avgIntensity * analysis.combinedConfidence).coerceIn(0.0f, 1.0f)
    }
    
    private suspend fun calculateAnalysisConfidence(
        facialAnalysis: FacialAnalysis,
        behavioralAnalysis: BehavioralAnalysis
    ): Float {
        val facialWeight = 0.6f
        val behavioralWeight = 0.4f
        
        return (facialAnalysis.confidence * facialWeight + 
                behavioralAnalysis.confidence * behavioralWeight)
    }
    
    private suspend fun assessLearningImpact(
        emotion: Emotion,
        intensity: Float,
        sessionData: LearningSessionData
    ): LearningImpact {
        return when (emotion.type) {
            EmotionType.HAPPY, EmotionType.EXCITED, EmotionType.CONFIDENT -> {
                if (intensity > 0.7f) LearningImpact.POSITIVE else LearningImpact.NEUTRAL
            }
            EmotionType.FRUSTRATED, EmotionType.ANXIOUS, EmotionType.SAD -> {
                if (intensity > 0.6f) LearningImpact.NEGATIVE else LearningImpact.NEUTRAL
            }
            EmotionType.BORED -> {
                if (intensity > 0.5f) LearningImpact.NEGATIVE else LearningImpact.NEUTRAL
            }
            else -> LearningImpact.NEUTRAL
        }
    }
    
    private suspend fun generateEmotionalRecommendations(
        emotion: Emotion,
        intensity: Float,
        impact: LearningImpact
    ): List<String> {
        val recommendations = mutableListOf<String>()
        
        when (impact) {
            LearningImpact.POSITIVE -> {
                recommendations.add("Maintain this positive emotional state")
                recommendations.add("Leverage enthusiasm for challenging topics")
                recommendations.add("Encourage peer collaboration")
            }
            LearningImpact.NEGATIVE -> {
                when (emotion.type) {
                    EmotionType.FRUSTRATED -> {
                        recommendations.add("Take a short break")
                        recommendations.add("Simplify the current task")
                        recommendations.add("Provide additional support")
                    }
                    EmotionType.ANXIOUS -> {
                        recommendations.add("Create a calm learning environment")
                        recommendations.add("Break down complex tasks")
                        recommendations.add("Offer reassurance and guidance")
                    }
                    EmotionType.BORED -> {
                        recommendations.add("Increase task complexity")
                        recommendations.add("Add interactive elements")
                        recommendations.add("Introduce new challenges")
                    }
                    else -> {
                        recommendations.add("Monitor emotional state")
                        recommendations.add("Provide appropriate support")
                    }
                }
            }
            LearningImpact.NEUTRAL -> {
                recommendations.add("Maintain current learning pace")
                recommendations.add("Monitor for emotional changes")
            }
        }
        
        return recommendations
    }
    
    private suspend fun generateFallbackEmotionalAnalysis(
        sessionData: LearningSessionData
    ): EmotionalAnalysis {
        return EmotionalAnalysis(
            id = "fallback_${sessionData.studentId}",
            studentId = sessionData.studentId,
            sessionId = sessionData.sessionId,
            timestamp = Date(),
            primaryEmotion = Emotion(
                type = EmotionType.CALM,
                intensity = 0.5f,
                duration = 0,
                context = "fallback",
                confidence = 0.3f
            ),
            emotionIntensity = 0.5f,
            secondaryEmotions = emptyList(),
            confidence = 0.3f,
            facialExpressions = emptyList(),
            behavioralPatterns = emptyList(),
            learningImpact = LearningImpact.NEUTRAL,
            recommendations = listOf("Unable to analyze emotions. Please check camera and sensor data.")
        )
    }
    
    // Additional helper methods would be implemented here...
    private suspend fun analyzeInteractionPatterns(interactions: List<InteractionData>): InteractionAnalysis = InteractionAnalysis()
    private suspend fun analyzePerformanceTrends(metrics: PerformanceMetrics): PerformanceAnalysis = PerformanceAnalysis()
    private suspend fun detectFrustrationIndicators(interaction: InteractionAnalysis, performance: PerformanceAnalysis): List<FrustrationIndicator> = emptyList()
    private suspend fun calculateFrustrationLevel(indicators: List<FrustrationIndicator>): FrustrationLevel = FrustrationLevel.NONE
    private suspend fun identifyFrustrationTriggers(interaction: InteractionAnalysis, performance: PerformanceAnalysis, indicators: List<FrustrationIndicator>): List<String> = emptyList()
    private suspend fun assessFrustrationImpact(level: FrustrationLevel, metrics: PerformanceMetrics): LearningImpact = LearningImpact.NEUTRAL
    private suspend fun generateFrustrationInterventions(level: FrustrationLevel, triggers: List<String>, impact: LearningImpact): List<String> = emptyList()
    private suspend fun calculateFrustrationUrgency(level: FrustrationLevel, impact: LearningImpact): Urgency = Urgency.LOW
    private suspend fun calculateFrustrationDuration(interactions: List<InteractionData>): Int = 0
    private suspend fun generateFallbackFrustrationDetection(studentId: String): FrustrationDetection = FrustrationDetection()
    private suspend fun analyzeEmotionalState(state: EmotionalState, context: String): EmotionalAnalysis = EmotionalAnalysis()
    private suspend fun generateSupportMessage(state: EmotionalState, context: String, analysis: EmotionalAnalysis): String = "Support message"
    private suspend fun determineSupportType(state: EmotionalState, analysis: EmotionalAnalysis): SupportType = SupportType.ENCOURAGEMENT
    private suspend fun generateSupportResources(state: EmotionalState, type: SupportType, studentId: String): List<SupportResource> = emptyList()
    private suspend fun planFollowUpActions(state: EmotionalState, type: SupportType, previous: List<SupportMessage>): List<String> = emptyList()
    private suspend fun predictSupportOutcome(state: EmotionalState, type: SupportType, resources: List<SupportResource>): String = "Expected outcome"
    private suspend fun calculateSupportConfidence(state: EmotionalState, type: SupportType, previous: List<SupportMessage>): Float = 0.7f
    private suspend fun generateFallbackEmotionalSupport(studentId: String, state: EmotionalState): EmotionalSupport = EmotionalSupport()
    private suspend fun analyzeResponsePatterns(responses: List<EmotionalResponse>): ResponsePatterns = ResponsePatterns()
    private suspend fun assessChallengeCharacteristics(challenge: LearningChallenge): ChallengeAssessment = ChallengeAssessment()
    private suspend fun identifyEmotionalRiskFactors(patterns: ResponsePatterns, assessment: ChallengeAssessment, response: EmotionalResponse): List<String> = emptyList()
    private suspend fun generatePreventiveMeasures(risks: List<String>, response: EmotionalResponse): List<String> = emptyList()
    private suspend fun developSupportStrategies(response: EmotionalResponse, risks: List<String>, measures: List<String>): List<String> = emptyList()
    private suspend fun calculatePredictionConfidence(patterns: ResponsePatterns, assessment: ChallengeAssessment): Float = 0.7f
    private suspend fun generateFallbackEmotionalResponsePrediction(studentId: String, challenge: LearningChallenge): EmotionalResponsePrediction = EmotionalResponsePrediction()
    private suspend fun gatherEmotionalData(studentId: String, range: TimeRange): List<EmotionalData> = emptyList()
    private suspend fun analyzeEmotionalTrends(data: List<EmotionalData>): EmotionalTrends = EmotionalTrends()
    private suspend fun identifyEmotionalPatterns(data: List<EmotionalData>): EmotionalPatterns = EmotionalPatterns()
    private suspend fun calculateWellbeingScore(trends: EmotionalTrends, patterns: EmotionalPatterns): Float = 0.7f
    private suspend fun generateWellbeingInsights(trends: EmotionalTrends, patterns: EmotionalPatterns): List<String> = emptyList()
    private suspend fun recommendWellbeingImprovements(score: Float, insights: List<String>, patterns: EmotionalPatterns): List<String> = emptyList()
    private suspend fun calculateWellbeingConfidence(data: List<EmotionalData>): Float = 0.7f
    private suspend fun generateFallbackWellbeingReport(studentId: String, range: TimeRange): EmotionalWellbeingReport = EmotionalWellbeingReport()
    private suspend fun analyzeEmotionalProfile(profile: EmotionalProfile): ProfileAnalysis = ProfileAnalysis()
    private suspend fun generateGoalSpecificStrategies(goal: String, profile: EmotionalProfile, analysis: ProfileAnalysis): List<EmotionalLearningStrategy> = emptyList()
    private suspend fun generateGeneralEmotionalStrategies(profile: EmotionalProfile): List<EmotionalLearningStrategy> = emptyList()
    private suspend fun prioritizeStrategies(strategies: List<EmotionalLearningStrategy>, profile: EmotionalProfile): List<EmotionalLearningStrategy> = strategies
    private suspend fun enrichStrategy(strategy: EmotionalLearningStrategy, profile: EmotionalProfile): EmotionalLearningStrategy = strategy
    private suspend fun generateFallbackEmotionalStrategies(studentId: String, goals: List<String>): List<EmotionalLearningStrategy> = emptyList()
}

// MARK: - Supporting Data Classes

data class CombinedEmotionalAnalysis(
    val facialConfidence: Float,
    val behavioralConfidence: Float,
    val combinedConfidence: Float,
    val emotions: List<Emotion>,
    val patterns: List<BehavioralPattern>
)

data class FacialAnalysis(
    val confidence: Float,
    val emotions: List<Emotion>,
    val expressions: List<FacialExpression>
)

data class BehavioralAnalysis(
    val confidence: Float,
    val patterns: List<BehavioralPattern>,
    val trends: List<BehavioralTrend>
)

data class InteractionAnalysis(
    val patterns: List<InteractionPattern> = emptyList(),
    val frequency: Map<String, Int> = emptyMap(),
    val duration: Map<String, Int> = emptyMap()
)

data class InteractionPattern(
    val type: String,
    val frequency: Int,
    val duration: Int,
    val context: String
)

data class PerformanceAnalysis(
    val trends: List<PerformanceTrend> = emptyList(),
    val patterns: List<PerformancePattern> = emptyList(),
    val anomalies: List<PerformanceAnomaly> = emptyList()
)

data class PerformanceTrend(
    val metric: String,
    val direction: String,
    val strength: Float,
    val duration: Int
)

data class PerformancePattern(
    val type: String,
    val frequency: Int,
    val impact: Float
)

data class PerformanceAnomaly(
    val type: String,
    val severity: Float,
    val description: String
)

data class FrustrationIndicator(
    val type: String,
    val strength: Float,
    val duration: Int,
    val context: String
)

data class EmotionalProfile(
    val studentId: String = "",
    val emotionalStrengths: List<String> = emptyList(),
    val emotionalChallenges: List<String> = emptyList(),
    val copingStrategies: List<String> = emptyList(),
    val triggers: List<String> = emptyList()
)

data class ProfileAnalysis(
    val strengths: List<String> = emptyList(),
    val challenges: List<String> = emptyList(),
    val recommendations: List<String> = emptyList()
)

data class EmotionalLearningStrategy(
    val id: String = "",
    val title: String = "",
    val description: String = "",
    val emotionalFocus: String = "",
    val implementation: String = "",
    val expectedOutcome: String = "",
    val difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
)

data class EmotionalData(
    val timestamp: Date,
    val emotion: EmotionType,
    val intensity: Float,
    val context: String,
    val source: String
)

data class EmotionalTrends(
    val overallTrend: String = "stable",
    val weeklyPatterns: List<WeeklyPattern> = emptyList(),
    val monthlyCycles: List<MonthlyCycle> = emptyList()
)

data class WeeklyPattern(
    val dayOfWeek: String,
    val averageEmotion: EmotionType,
    val averageIntensity: Float
)

data class MonthlyCycle(
    val weekOfMonth: Int,
    val dominantEmotion: EmotionType,
    val emotionalStability: Float
)

data class EmotionalPatterns(
    val recurringPatterns: List<RecurringPattern> = emptyList(),
    val triggerPatterns: List<TriggerPattern> = emptyList(),
    val responsePatterns: List<ResponsePattern> = emptyList()
)

data class RecurringPattern(
    val type: String,
    val frequency: String,
    val description: String
)

data class TriggerPattern(
    val trigger: String,
    val response: EmotionType,
    val intensity: Float
)

data class ResponsePattern(
    val stimulus: String,
    val response: EmotionType,
    val duration: Int
)

data class LearningChallenge(
    val id: String = "",
    val title: String = "",
    val description: String = "",
    val difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
    val subject: String = "",
    val estimatedDuration: Int = 0
)

data class ChallengeAssessment(
    val complexity: Float = 0.5f,
    val novelty: Float = 0.5f,
    val stressLevel: Float = 0.5f,
    val supportAvailable: Float = 0.7f
)

data class EmotionalResponse(
    val id: String = "",
    val studentId: String = "",
    val challenge: LearningChallenge,
    val response: EmotionType,
    val intensity: Float,
    val duration: Int,
    val context: String
)

data class ResponsePatterns(
    val commonResponses: List<CommonResponse> = emptyList(),
    val stressResponses: List<StressResponse> = emptyList(),
    val successResponses: List<SuccessResponse> = emptyList()
)

data class CommonResponse(
    val stimulus: String,
    val response: EmotionType,
    val frequency: Int,
    val averageIntensity: Float
)

data class StressResponse(
    val stressLevel: Float,
    val response: EmotionType,
    val copingMechanism: String
)

data class SuccessResponse(
    val achievement: String,
    val response: EmotionType,
    val celebration: String
)

data class LearningSessionData(
    val sessionId: String,
    val studentId: String,
    val startTime: Date,
    val endTime: Date?,
    val subject: String,
    val activities: List<String>
)

data class InteractionData(
    val id: String,
    val studentId: String,
    val timestamp: Date,
    val type: String,
    val content: String,
    val response: String?
)

data class PerformanceMetrics(
    val accuracy: Float,
    val speed: Float,
    val engagement: Float,
    val completion: Float
)

data class SupportMessage(
    val id: String,
    val studentId: String,
    val message: String,
    val timestamp: Date,
    val effectiveness: Float
)

data class TimeRange(
    val start: Date,
    val end: Date,
    val type: String = "custom"
)

// MARK: - Exceptions

class EmotionalIntelligenceException(message: String) : Exception(message)