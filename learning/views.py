from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import (
    Subject, LearningPath, Lesson, LessonProgress, Assignment, AssignmentSubmission,
    Quiz, Question, QuizAttempt, StudentPortfolio
)
from .serializers import (
    SubjectSerializer, LearningPathSerializer, LessonSerializer, LessonProgressSerializer,
    AssignmentSerializer, AssignmentSubmissionSerializer, QuizSerializer, QuestionSerializer,
    QuizAttemptSerializer, StudentPortfolioSerializer, StudentProgressSummarySerializer
)
from accounts.models import Student


class SubjectViewSet(viewsets.ModelViewSet):
    """Subject viewset"""
    queryset = Subject.objects.filter(is_active=True)
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        grade_level = self.request.query_params.get('grade_level')
        if grade_level:
            queryset = queryset.filter(grade_levels__contains=[grade_level])
        return queryset


class LearningPathViewSet(viewsets.ModelViewSet):
    """Learning path viewset"""
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return LearningPath.objects.filter(student__user=user, is_active=True)
        elif user.role == 'staff':
            return LearningPath.objects.filter(
                student__in=user.staff_profile.assigned_students.all(),
                is_active=True
            )
        elif user.role == 'admin':
            return LearningPath.objects.filter(is_active=True)
        return LearningPath.objects.none()


class LessonViewSet(viewsets.ModelViewSet):
    """Lesson viewset"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Lesson.objects.filter(
                learning_path__student__user=user,
                is_active=True
            ).order_by('learning_path', 'order')
        elif user.role in ['staff', 'admin']:
            return Lesson.objects.filter(is_active=True).order_by('learning_path', 'order')
        return Lesson.objects.none()


class AssignmentViewSet(viewsets.ModelViewSet):
    """Assignment viewset"""
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Assignment.objects.filter(
                assigned_to=user.student_profile,
                status='published'
            ).order_by('-due_date')
        elif user.role == 'staff':
            return Assignment.objects.filter(created_by=user.staff_profile)
        elif user.role == 'admin':
            return Assignment.objects.all()
        return Assignment.objects.none()


class QuizViewSet(viewsets.ModelViewSet):
    """Quiz viewset"""
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Quiz.objects.filter(is_active=True)
        elif user.role in ['staff', 'admin']:
            return Quiz.objects.all()
        return Quiz.objects.none()


class QuestionViewSet(viewsets.ModelViewSet):
    """Question viewset"""
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['staff', 'admin']:
            return Question.objects.all().order_by('quiz', 'order')
        elif user.role == 'student':
            return Question.objects.filter(quiz__is_active=True).order_by('quiz', 'order')
        return Question.objects.none()


class StudentPortfolioViewSet(viewsets.ModelViewSet):
    """Student portfolio viewset"""
    serializer_class = StudentPortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return StudentPortfolio.objects.filter(student__user=user)
        elif user.role == 'family':
            return StudentPortfolio.objects.filter(
                student__in=user.family_profile.students.all(),
                is_public=True
            )
        elif user.role in ['staff', 'admin']:
            return StudentPortfolio.objects.all()
        return StudentPortfolio.objects.none()


class LearningProgressView(generics.RetrieveAPIView):
    """Get learning progress for current user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can view learning progress'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student = request.user.student_profile
        learning_paths = LearningPath.objects.filter(student=student, is_active=True)
        progress_data = []
        
        for path in learning_paths:
            lessons = path.lessons.all()
            completed_lessons = LessonProgress.objects.filter(
                lesson__in=lessons,
                student=student,
                status='completed'
            ).count()
            
            progress_data.append({
                'learning_path': LearningPathSerializer(path).data,
                'total_lessons': lessons.count(),
                'completed_lessons': completed_lessons,
                'progress_percentage': (completed_lessons / lessons.count() * 100) if lessons.count() > 0 else 0
            })
        
        return Response(progress_data)


class StudentProgressView(generics.RetrieveAPIView):
    """Get progress for a specific student"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id):
        if request.user.role not in ['staff', 'admin', 'family']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student = get_object_or_404(Student, id=student_id)
        progress_summary = self._calculate_student_progress(student)
        return Response(progress_summary)
    
    def _calculate_student_progress(self, student):
        """Calculate comprehensive progress summary for a student"""
        learning_paths = LearningPath.objects.filter(student=student, is_active=True)
        completed_lessons = LessonProgress.objects.filter(
            student=student,
            status='completed'
        ).count()
        
        total_lessons = Lesson.objects.filter(
            learning_path__student=student,
            is_active=True
        ).count()
        
        return {
            'student': student.id,
            'student_name': student.user.get_full_name(),
            'total_learning_paths': learning_paths.count(),
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'completion_percentage': (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        }


class LessonProgressView(generics.CreateAPIView, generics.UpdateAPIView):
    """Update lesson progress"""
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        lesson_id = self.kwargs['lesson_id']
        student = self.request.user.student_profile
        progress, created = LessonProgress.objects.get_or_create(
            lesson_id=lesson_id,
            student=student
        )
        return progress


class AssignmentSubmissionView(generics.CreateAPIView):
    """Submit assignment"""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise permissions.PermissionDenied('Only students can submit assignments')
        
        assignment_id = self.kwargs['assignment_id']
        assignment = get_object_or_404(Assignment, id=assignment_id)
        
        is_late = timezone.now() > assignment.due_date
        
        serializer.save(
            student=self.request.user.student_profile,
            assignment=assignment,
            is_late=is_late,
            submitted_at=timezone.now(),
            status='submitted'
        )


class AssignmentSubmissionListView(generics.ListAPIView):
    """List assignment submissions"""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        user = self.request.user
        
        if user.role in ['staff', 'admin']:
            return AssignmentSubmission.objects.filter(assignment_id=assignment_id)
        elif user.role == 'student':
            return AssignmentSubmission.objects.filter(
                assignment_id=assignment_id,
                student__user=user
            )
        return AssignmentSubmission.objects.none()


class QuizAttemptView(generics.CreateAPIView, generics.UpdateAPIView):
    """Quiz attempt view"""
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        quiz_id = self.kwargs['quiz_id']
        student = self.request.user.student_profile
        return get_object_or_404(
            QuizAttempt,
            quiz_id=quiz_id,
            student=student,
            status='started'
        )


class QuizAttemptListView(generics.ListAPIView):
    """List quiz attempts"""
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        user = self.request.user
        
        if user.role in ['staff', 'admin']:
            return QuizAttempt.objects.filter(quiz_id=quiz_id)
        elif user.role == 'student':
            return QuizAttempt.objects.filter(
                quiz_id=quiz_id,
                student__user=user
            )
        return QuizAttempt.objects.none()


class StudentDashboardView(generics.RetrieveAPIView):
    """Student dashboard data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can access student dashboard'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student = request.user.student_profile
        
        recent_lessons = LessonProgress.objects.filter(
            student=student
        ).select_related('lesson').order_by('-last_accessed')[:5]
        
        upcoming_assignments = Assignment.objects.filter(
            assigned_to=student,
            status='published',
            due_date__gt=timezone.now()
        ).order_by('due_date')[:5]
        
        return Response({
            'recent_lessons': LessonProgressSerializer(recent_lessons, many=True).data,
            'upcoming_assignments': AssignmentSerializer(upcoming_assignments, many=True).data,
        })


class TeacherDashboardView(generics.RetrieveAPIView):
    """Teacher/Staff dashboard data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role not in ['staff', 'admin']:
            return Response(
                {'error': 'Access denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.role == 'staff':
            students = request.user.staff_profile.assigned_students.all()
        else:
            students = Student.objects.filter(is_active=True)
        
        return Response({
            'assigned_students_count': students.count(),
        })