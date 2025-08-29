from django.contrib import admin
from .models import (
    Subject, LearningPath, Lesson, LessonProgress, Assignment, AssignmentSubmission,
    Quiz, Question, QuizAttempt, StudentPortfolio
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Subject admin"""
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """Learning path admin"""
    list_display = [
        'name', 'student', 'subject', 'difficulty_level', 
        'estimated_duration_hours', 'is_active', 'created_by_ai'
    ]
    list_filter = ['difficulty_level', 'is_active', 'created_by_ai', 'subject']
    search_fields = ['name', 'student__user__first_name', 'student__user__last_name']
    ordering = ['-created_at']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin"""
    list_display = [
        'title', 'learning_path', 'lesson_type', 'order',
        'estimated_duration_minutes', 'difficulty_level', 'is_mandatory', 'is_active'
    ]
    list_filter = ['lesson_type', 'difficulty_level', 'is_mandatory', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['learning_path', 'order']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Assignment admin"""
    list_display = [
        'title', 'subject', 'assignment_type', 'created_by',
        'due_date', 'max_score', 'status'
    ]
    list_filter = ['assignment_type', 'status', 'subject', 'due_date']
    search_fields = ['title', 'description']
    filter_horizontal = ['assigned_to']
    ordering = ['-due_date']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Quiz admin"""
    list_display = [
        'title', 'subject', 'quiz_type', 'time_limit_minutes',
        'max_attempts', 'passing_score', 'is_active'
    ]
    list_filter = ['quiz_type', 'is_active', 'subject']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


class QuestionInline(admin.TabularInline):
    """Question inline for Quiz admin"""
    model = Question
    extra = 1
    fields = ['order', 'question_text', 'question_type', 'points', 'difficulty_level']


# Add inline to Quiz admin
QuizAdmin.inlines = [QuestionInline]


@admin.register(StudentPortfolio)
class StudentPortfolioAdmin(admin.ModelAdmin):
    """Student portfolio admin"""
    list_display = [
        'title', 'student', 'item_type', 'subject',
        'is_public', 'is_featured', 'created_at'
    ]
    list_filter = ['item_type', 'is_public', 'is_featured', 'subject']
    search_fields = ['title', 'description', 'student__user__first_name']
    ordering = ['-created_at']