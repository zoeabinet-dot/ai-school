from rest_framework import serializers
from .models import (
    Subject, LearningPath, Lesson, LessonProgress, Assignment, AssignmentSubmission,
    Quiz, Question, QuizAttempt, StudentPortfolio
)
from accounts.models import Student


class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer"""
    
    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'description', 'grade_levels', 
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'learning_path', 'title', 'description', 'lesson_type',
            'content', 'order', 'estimated_duration_minutes', 'difficulty_level',
            'learning_objectives', 'resources', 'is_mandatory', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LearningPathSerializer(serializers.ModelSerializer):
    """Learning path serializer"""
    
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'student', 'subject', 'name', 'description', 'difficulty_level',
            'estimated_duration_hours', 'prerequisites_met', 'is_active',
            'created_by_ai', 'lessons', 'lessons_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonProgressSerializer(serializers.ModelSerializer):
    """Lesson progress serializer"""
    
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = LessonProgress
        fields = [
            'id', 'student', 'lesson', 'lesson_id', 'status', 'score',
            'time_spent_minutes', 'attempts', 'started_at', 'completed_at',
            'last_accessed', 'notes'
        ]
        read_only_fields = ['id', 'last_accessed']


class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment serializer"""
    
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'assignment_type', 'subject', 'subject_name',
            'learning_path', 'assigned_to', 'created_by', 'created_by_name',
            'due_date', 'max_score', 'instructions', 'resources', 'rubric',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """Assignment submission serializer"""
    
    assignment = AssignmentSerializer(read_only=True)
    assignment_id = serializers.IntegerField(write_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    graded_by_name = serializers.CharField(source='graded_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_id', 'student', 'student_name',
            'content', 'files', 'submitted_at', 'status', 'score', 'feedback',
            'graded_by', 'graded_by_name', 'graded_at', 'is_late',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_late', 'created_at', 'updated_at']


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer"""
    
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'question_text', 'question_type', 'options',
            'correct_answer', 'explanation', 'points', 'order', 'difficulty_level'
        ]
        read_only_fields = ['id']


class QuizSerializer(serializers.ModelSerializer):
    """Quiz serializer"""
    
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    total_points = serializers.DecimalField(source='questions.aggregate', max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'quiz_type', 'subject', 'lesson',
            'time_limit_minutes', 'max_attempts', 'passing_score',
            'is_randomized', 'show_results_immediately', 'is_active',
            'questions', 'questions_count', 'total_points', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Quiz attempt serializer"""
    
    quiz = QuizSerializer(read_only=True)
    quiz_id = serializers.IntegerField(write_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    percentage_score = serializers.SerializerMethodField()
    
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz', 'quiz_id', 'student', 'student_name', 'attempt_number',
            'status', 'score', 'total_points', 'percentage_score', 'answers',
            'started_at', 'completed_at', 'time_spent_minutes'
        ]
        read_only_fields = ['id', 'started_at']
    
    def get_percentage_score(self, obj):
        if obj.score and obj.total_points:
            return round((obj.score / obj.total_points) * 100, 2)
        return None


class StudentPortfolioSerializer(serializers.ModelSerializer):
    """Student portfolio serializer"""
    
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = StudentPortfolio
        fields = [
            'id', 'student', 'student_name', 'title', 'description',
            'item_type', 'subject', 'subject_name', 'files', 'tags',
            'reflection', 'is_public', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentProgressSummarySerializer(serializers.Serializer):
    """Student progress summary serializer"""
    
    student = serializers.IntegerField()
    student_name = serializers.CharField()
    total_learning_paths = serializers.IntegerField()
    completed_learning_paths = serializers.IntegerField()
    in_progress_learning_paths = serializers.IntegerField()
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_study_time_hours = serializers.DecimalField(max_digits=8, decimal_places=2)
    assignments_completed = serializers.IntegerField()
    assignments_pending = serializers.IntegerField()
    quiz_attempts = serializers.IntegerField()
    average_quiz_score = serializers.DecimalField(max_digits=5, decimal_places=2)