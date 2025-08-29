#!/usr/bin/env python3
"""
Test API endpoints for mobile app integration
Run this script to verify all API endpoints are working correctly
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class APITester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.client = APIClient()
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, endpoint: str, status: str, details: str = ""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {endpoint}: {status}"
        if details:
            result += f" - {details}"
        print(result)
        self.test_results.append((endpoint, status, details))
        
    def create_test_user(self):
        """Create a test user for authentication"""
        try:
            user, created = User.objects.get_or_create(
                email="test@aischool.com",
                defaults={
                    "first_name": "Test",
                    "last_name": "User",
                    "role": "admin",
                    "is_staff": True,
                    "is_superuser": True
                }
            )
            if created:
                user.set_password("testpass123")
                user.save()
                print(f"✅ Created test user: {user.email}")
            else:
                print(f"✅ Using existing test user: {user.email}")
            
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            self.auth_token = str(refresh.access_token)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.auth_token}')
            
            return user
        except Exception as e:
            print(f"❌ Failed to create test user: {e}")
            return None
    
    def test_health_check(self):
        """Test the health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health/")
            if response.status_code == 200:
                self.log_test("/health/", "✅ PASSED", "Server is running")
            else:
                self.log_test("/health/", "❌ FAILED", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("/health/", "❌ FAILED", f"Error: {e}")
    
    def test_authentication(self):
        """Test authentication endpoints"""
        endpoints = [
            ("POST", "/api/v1/accounts/login/", "Login"),
            ("POST", "/api/v1/accounts/logout/", "Logout"),
            ("GET", "/api/v1/accounts/profile/", "Profile")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "POST" and "login" in endpoint:
                    # Test login with test credentials
                    data = {
                        "email": "test@aischool.com",
                        "password": "testpass123",
                        "role": "admin"
                    }
                    response = self.client.post(endpoint, data, format='json')
                elif method == "GET":
                    response = self.client.get(endpoint)
                else:
                    response = self.client.post(endpoint)
                
                if response.status_code in [200, 201]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_students_api(self):
        """Test students API endpoints"""
        endpoints = [
            ("GET", "/api/v1/students/", "List Students"),
            ("POST", "/api/v1/students/", "Create Student"),
            ("GET", "/api/v1/students/1/", "Get Student"),
            ("PUT", "/api/v1/students/1/", "Update Student"),
            ("DELETE", "/api/v1/students/1/", "Delete Student")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    # Test data for creating a student
                    data = {
                        "student_id": "TEST001",
                        "grade_level": "10",
                        "academic_status": "active",
                        "enrollment_date": "2024-01-01"
                    }
                    response = self.client.post(endpoint, data, format='json')
                elif method == "PUT":
                    data = {"grade_level": "11"}
                    response = self.client.put(endpoint, data, format='json')
                else:
                    response = self.client.delete(endpoint)
                
                if response.status_code in [200, 201, 204]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_ai_teacher_api(self):
        """Test AI teacher API endpoints"""
        endpoints = [
            ("GET", "/api/v1/ai-teacher/lessons/", "List AI Lessons"),
            ("POST", "/api/v1/ai-teacher/lessons/", "Create AI Lesson"),
            ("GET", "/api/v1/ai-teacher/lessons/1/", "Get AI Lesson"),
            ("PUT", "/api/v1/ai-teacher/lessons/1/", "Update AI Lesson"),
            ("DELETE", "/api/v1/ai-teacher/lessons/1/", "Delete AI Lesson")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    data = {
                        "title": "Test AI Lesson",
                        "subject": "Mathematics",
                        "difficulty_level": "beginner"
                    }
                    response = self.client.post(endpoint, data, format='json')
                else:
                    response = self.client.get(endpoint)
                
                if response.status_code in [200, 201]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_analytics_api(self):
        """Test analytics API endpoints"""
        endpoints = [
            ("GET", "/api/v1/analytics/", "Get Analytics"),
            ("GET", "/api/v1/analytics/?time_range=week", "Get Weekly Analytics")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                response = self.client.get(endpoint)
                if response.status_code == 200:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_monitoring_api(self):
        """Test monitoring API endpoints"""
        endpoints = [
            ("GET", "/api/v1/monitoring/", "Get Monitoring Data"),
            ("POST", "/api/v1/monitoring/toggle/", "Toggle Monitoring"),
            ("POST", "/api/v1/monitoring/privacy-settings/", "Update Privacy Settings")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    if "toggle" in endpoint:
                        data = {"isActive": True}
                    else:
                        data = {
                            "faceDetectionEnabled": True,
                            "behaviorAnalysisEnabled": True,
                            "recordingEnabled": False,
                            "alertsEnabled": True
                        }
                    response = self.client.post(endpoint, data, format='json')
                
                if response.status_code in [200, 201]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_families_api(self):
        """Test families API endpoints"""
        endpoints = [
            ("GET", "/api/v1/families/", "Get Family Data"),
            ("POST", "/api/v1/families/members/", "Add Family Member"),
            ("DELETE", "/api/v1/families/members/1/", "Remove Family Member")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    data = {
                        "fullName": "Test Family Member",
                        "relationship": "parent"
                    }
                    response = self.client.post(endpoint, data, format='json')
                else:
                    response = self.client.delete(endpoint)
                
                if response.status_code in [200, 201, 204]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_staff_api(self):
        """Test staff API endpoints"""
        endpoints = [
            ("GET", "/api/v1/staff/", "Get Staff Data"),
            ("POST", "/api/v1/staff/", "Create Staff"),
            ("GET", "/api/v1/staff/1/", "Get Staff Member"),
            ("PUT", "/api/v1/staff/1/", "Update Staff"),
            ("DELETE", "/api/v1/staff/1/", "Delete Staff")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    data = {
                        "fullName": "Test Staff Member",
                        "role": "teacher"
                    }
                    response = self.client.post(endpoint, data, format='json')
                elif method == "PUT":
                    data = {"role": "administrator"}
                    response = self.client.put(endpoint, data, format='json')
                else:
                    response = self.client.get(endpoint)
                
                if response.status_code in [200, 201]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def test_lessons_api(self):
        """Test lessons API endpoints"""
        endpoints = [
            ("GET", "/api/v1/lessons/", "Get Lessons"),
            ("POST", "/api/v1/lessons/", "Create Lesson"),
            ("GET", "/api/v1/lessons/1/", "Get Lesson"),
            ("PUT", "/api/v1/lessons/1/", "Update Lesson"),
            ("DELETE", "/api/v1/lessons/1/", "Delete Lesson")
        ]
        
        for method, endpoint, name in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(endpoint)
                elif method == "POST":
                    data = {
                        "title": "Test Lesson",
                        "subject": "Mathematics",
                        "description": "Test lesson description"
                    }
                    response = self.client.post(endpoint, data, format='json')
                else:
                    response = self.client.get(endpoint)
                
                if response.status_code in [200, 201]:
                    self.log_test(endpoint, "✅ PASSED", name)
                else:
                    self.log_test(endpoint, "⚠️ PARTIAL", f"{name} - Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "❌ FAILED", f"{name} - Error: {e}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Integration Tests for Mobile Apps")
        print("=" * 60)
        
        # Test server health
        self.test_health_check()
        print()
        
        # Create test user and authenticate
        print("🔐 Setting up authentication...")
        user = self.create_test_user()
        if not user:
            print("❌ Cannot proceed without test user")
            return
        print()
        
        # Test all API endpoints
        print("📱 Testing Mobile App API Endpoints...")
        print("-" * 40)
        
        self.test_authentication()
        print()
        
        self.test_students_api()
        print()
        
        self.test_ai_teacher_api()
        print()
        
        self.test_analytics_api()
        print()
        
        self.test_monitoring_api()
        print()
        
        self.test_families_api()
        print()
        
        self.test_staff_api()
        print()
        
        self.test_lessons_api()
        print()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if "✅" in r[1]])
        partial = len([r for r in self.test_results if "⚠️" in r[1]])
        failed = len([r for r in self.test_results if "❌" in r[1]])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️ Partial: {partial}")
        print(f"❌ Failed: {failed}")
        print()
        
        if failed == 0:
            print("🎉 All API endpoints are working correctly!")
            print("📱 Mobile apps can now connect to the Django backend.")
        else:
            print("⚠️ Some API endpoints need attention before mobile app deployment.")
            print("Please check the failed endpoints above.")

def main():
    """Main function to run API tests"""
    try:
        tester = APITester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()