import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_school_management.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from students.models import Student
from families.models import Family
from staff.models import Staff, StaffProfile
from lessons.models import Lesson
from ai_teacher.models import AILesson
from analytics.models import LearningAnalytics
from datetime import datetime, timedelta
import json

User = get_user_model()

def create_test_data():
    try:
        # Clean up any existing test data first
        print("Cleaning up existing test data...")
        User.objects.filter(username__startswith='test_').delete()

        # Create test users with different roles
        print("Creating test users...")
        student_user = User.objects.create_user(
            username='test_student',
            email='student@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Student',
            role=User.UserRole.STUDENT
        )
        
        parent_user = User.objects.create_user(
            username='test_parent',
            email='parent@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Parent',
            role=User.UserRole.FAMILY
        )
        
        teacher_user = User.objects.create_user(
            username='test_teacher',
            email='teacher@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Teacher',
            role=User.UserRole.STAFF
        )

        # Create a test family
        print("Creating test family...")
        family = Family.objects.create(
            user=parent_user,
            family_name='Test',
            primary_contact_name='Test Parent',
            primary_contact_email='parent@example.com',
            primary_contact_phone='+1234567890',
            address='123 Test St',
            location='Test City',
            emergency_contact={
                'name': 'Emergency Contact',
                'phone': '+1987654321',
                'relationship': 'Grandparent'
            }
        )

        # Create a test student
        print("Creating test student...")
        student = Student.objects.create(
            user=student_user,
            student_id='TEST001',
            grade_level='8',
            academic_year='2023-2024',
            enrollment_date='2023-09-01',
            learning_style='visual'
        )

        # Create a test staff member
        print("Creating test staff member...")
        staff = Staff.objects.create(
            user=teacher_user,
            employee_id='EMP001',
            department=Staff.Department.TEACHING,
            role=Staff.StaffRole.TEACHER,
            hire_date=datetime.now().date(),
            qualifications=['Bachelor of Education', 'Teaching Certificate'],
            specializations=['Mathematics', 'Computer Science']
        )
        
        # Create staff profile
        StaffProfile.objects.create(
            staff=staff,
            assigned_grades=['8'],  # Same grade level as our test student
            assigned_subjects=['Mathematics', 'Computer Science'],
            teaching_experience=5,
            certifications=['National Board Certification'],
            preferences={
                'communication_method': 'email',
                'notification_frequency': 'daily'
            }
        )

        # Create test lessons
        print("Creating test lessons...")
        for i in range(1, 4):
            lesson = Lesson.objects.create(
                title=f'Test Lesson {i}',
                description=f'Description for test lesson {i}',
                subject=Lesson.Subject.MATHEMATICS,
                grade_level='8',
                lesson_type=Lesson.LessonType.INTERACTIVE,
                difficulty=Lesson.Difficulty.INTERMEDIATE,
                duration_minutes=45,
                learning_objectives=[
                    'Understand basic mathematical concepts',
                    'Apply problem-solving skills',
                    'Demonstrate critical thinking'
                ]
            )

            # Create AI-enhanced version of the lesson
            AILesson.objects.create(
                title=f'AI Enhanced Lesson {i}',
                description=f'AI-enhanced version of Test Lesson {i}',
                subject='Mathematics',
                grade_level='8',
                difficulty_level='intermediate',
                lesson_type='interactive',
                content={
                    'introduction': f'AI-generated introduction for lesson {i}',
                    'main_content': [
                        {'type': 'explanation', 'text': f'AI-generated explanation {i}'},
                        {'type': 'example', 'text': f'AI-generated example {i}'},
                        {'type': 'practice', 'problems': [f'Problem {j}' for j in range(1, 4)]}
                    ],
                    'conclusion': f'AI-generated conclusion for lesson {i}'
                },
                learning_objectives=[
                    'Master key concepts through AI-guided learning',
                    'Practice with adaptive difficulty',
                    'Receive personalized feedback'
                ],
                prerequisites=['Basic math understanding'],
                ai_model_used='GPT-4',
                ai_generation_prompt=f'Create an interactive math lesson about topic {i}',
                ai_parameters={'temperature': 0.7, 'max_tokens': 1000},
                estimated_duration=45
            )

        # Create test analytics data
        print("Creating test analytics data...")
        for i in range(7):
            date = datetime.now().date() - timedelta(days=i)
            LearningAnalytics.objects.create(
                student=student_user,
                date=date,
                total_learning_time=120 + i * 10,  # minutes
                active_learning_time=90 + i * 8,   # minutes
                sessions_started=3,
                sessions_completed=2,
                sessions_abandoned=1,
                average_attention_score=85.5 + i,
                average_engagement_score=88.0 + i,
                subject_performance=json.dumps({
                    'Mathematics': 85 + i,
                    'Science': 82 + i,
                    'English': 88 + i
                }),
                skill_progress=json.dumps({
                    'Problem Solving': 80 + i,
                    'Critical Thinking': 85 + i,
                    'Communication': 82 + i
                }),
                ai_conversations_count=5 + i,
                ai_recommendations_followed=3 + i,
                ai_lessons_completed=2 + i,
                learning_patterns=json.dumps({
                    'preferred_time': 'morning',
                    'common_breaks': ['11:00', '15:00'],
                    'most_productive_subject': 'Mathematics'
                }),
                attention_trends=json.dumps([85, 88, 90, 87, 89]),
                engagement_peaks=json.dumps([
                    {'time': '09:30', 'score': 95},
                    {'time': '11:30', 'score': 92}
                ])
            )

        print("Test data creation completed!")
    except Exception as e:
        print(f"Error in create_test_data: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        create_test_data()
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        raise
