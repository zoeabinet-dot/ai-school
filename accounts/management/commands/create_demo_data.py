from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, Student, Family, Staff, Administrator
from learning.models import Subject, LearningPath, Lesson
from ai_teacher.models import AITeacherProfile


class Command(BaseCommand):
    help = 'Create demo data for the school management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')
        
        # Create demo users
        self.create_demo_users()
        
        # Create subjects
        self.create_subjects()
        
        # Create AI teacher profile
        self.create_ai_teacher()
        
        # Create learning content
        self.create_learning_content()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created demo data!')
        )

    def create_demo_users(self):
        """Create demo users for each role"""
        
        # Create student user
        if not User.objects.filter(username='student_demo').exists():
            student_user = User.objects.create_user(
                username='student_demo',
                email='student@demo.com',
                password='demo123',
                first_name='Abebe',
                last_name='Kebede',
                role='student'
            )
            
            Student.objects.create(
                user=student_user,
                student_id='STU001',
                grade_level='8',
                enrollment_date=timezone.now().date(),
                learning_pace='medium',
                preferred_learning_style='visual',
                attention_span_minutes=45
            )
            self.stdout.write('Created student demo user')

        # Create family user
        if not User.objects.filter(username='family_demo').exists():
            family_user = User.objects.create_user(
                username='family_demo',
                email='family@demo.com',
                password='demo123',
                first_name='Almaz',
                last_name='Kebede',
                role='family'
            )
            
            family = Family.objects.create(
                user=family_user,
                relationship='parent',
                occupation='Teacher',
                preferred_communication='email'
            )
            
            # Link to student
            student = Student.objects.filter(student_id='STU001').first()
            if student:
                family.students.add(student)
            
            self.stdout.write('Created family demo user')

        # Create staff user
        if not User.objects.filter(username='staff_demo').exists():
            staff_user = User.objects.create_user(
                username='staff_demo',
                email='staff@demo.com',
                password='demo123',
                first_name='Dawit',
                last_name='Mengistu',
                role='staff'
            )
            
            staff = Staff.objects.create(
                user=staff_user,
                employee_id='EMP001',
                position='teacher_assistant',
                department='Mathematics',
                hire_date=timezone.now().date(),
                qualifications='Bachelor of Education in Mathematics'
            )
            
            # Assign student to staff
            student = Student.objects.filter(student_id='STU001').first()
            if student:
                staff.assigned_students.add(student)
            
            self.stdout.write('Created staff demo user')

        # Create admin user
        if not User.objects.filter(username='admin_demo').exists():
            admin_user = User.objects.create_user(
                username='admin_demo',
                email='admin@demo.com',
                password='demo123',
                first_name='Meron',
                last_name='Tadesse',
                role='admin'
            )
            
            Administrator.objects.create(
                user=admin_user,
                access_level='super',
                permissions={
                    'can_manage_users': True,
                    'can_view_all_data': True,
                    'can_modify_system': True
                },
                managed_departments=['All']
            )
            self.stdout.write('Created admin demo user')

    def create_subjects(self):
        """Create demo subjects"""
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH', 'grade_levels': ['7', '8', '9', '10']},
            {'name': 'English', 'code': 'ENG', 'grade_levels': ['7', '8', '9', '10']},
            {'name': 'Science', 'code': 'SCI', 'grade_levels': ['7', '8', '9', '10']},
            {'name': 'History', 'code': 'HIST', 'grade_levels': ['7', '8', '9', '10']},
            {'name': 'Amharic', 'code': 'AMH', 'grade_levels': ['7', '8', '9', '10']},
        ]
        
        for subject_data in subjects_data:
            if not Subject.objects.filter(code=subject_data['code']).exists():
                Subject.objects.create(
                    name=subject_data['name'],
                    code=subject_data['code'],
                    description=f'Grade level {subject_data["name"]} curriculum',
                    grade_levels=subject_data['grade_levels']
                )
                self.stdout.write(f'Created subject: {subject_data["name"]}')

    def create_ai_teacher(self):
        """Create AI teacher profile"""
        if not AITeacherProfile.objects.exists():
            AITeacherProfile.objects.create(
                name='Alpha AI Teacher',
                personality_type='encouraging',
                system_prompt='''You are Alpha, an AI teacher helping Ethiopian students in Addis Ababa. 
                You are encouraging, patient, and culturally aware. You adapt your teaching style to each 
                student's grade level and learning preferences. You use examples relevant to Ethiopian 
                culture and context when appropriate.''',
                specializations=['Mathematics', 'Science', 'English', 'General Learning Support'],
                language_preferences=['English', 'Amharic'],
                voice_settings={
                    'voice_type': 'female',
                    'speed': 'normal',
                    'pitch': 'medium'
                }
            )
            self.stdout.write('Created AI teacher profile')

    def create_learning_content(self):
        """Create demo learning content"""
        student = Student.objects.filter(student_id='STU001').first()
        math_subject = Subject.objects.filter(code='MATH').first()
        
        if student and math_subject:
            # Create learning path
            if not LearningPath.objects.filter(student=student, subject=math_subject).exists():
                learning_path = LearningPath.objects.create(
                    student=student,
                    subject=math_subject,
                    name='Grade 8 Mathematics Fundamentals',
                    description='Core mathematics concepts for grade 8 students',
                    difficulty_level='intermediate',
                    estimated_duration_hours=40,
                    prerequisites_met=True,
                    created_by_ai=True
                )
                
                # Create sample lessons
                lessons_data = [
                    {
                        'title': 'Introduction to Algebra',
                        'description': 'Basic algebraic concepts and variables',
                        'lesson_type': 'interactive',
                        'order': 1,
                        'estimated_duration_minutes': 45
                    },
                    {
                        'title': 'Solving Linear Equations',
                        'description': 'Methods for solving linear equations',
                        'lesson_type': 'video',
                        'order': 2,
                        'estimated_duration_minutes': 50
                    },
                    {
                        'title': 'Graphing Linear Functions',
                        'description': 'Understanding and graphing linear functions',
                        'lesson_type': 'interactive',
                        'order': 3,
                        'estimated_duration_minutes': 60
                    }
                ]
                
                for lesson_data in lessons_data:
                    Lesson.objects.create(
                        learning_path=learning_path,
                        title=lesson_data['title'],
                        description=lesson_data['description'],
                        lesson_type=lesson_data['lesson_type'],
                        order=lesson_data['order'],
                        estimated_duration_minutes=lesson_data['estimated_duration_minutes'],
                        difficulty_level='intermediate',
                        content={
                            'introduction': f'Welcome to {lesson_data["title"]}',
                            'main_content': lesson_data['description'],
                            'activities': ['Practice problems', 'Interactive exercises'],
                            'summary': f'You learned about {lesson_data["title"].lower()}'
                        },
                        learning_objectives=[
                            f'Understand {lesson_data["title"].lower()}',
                            'Apply concepts to solve problems',
                            'Demonstrate mastery through exercises'
                        ]
                    )
                
                self.stdout.write('Created sample learning content')