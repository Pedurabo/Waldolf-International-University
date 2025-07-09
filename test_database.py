#!/usr/bin/env python3
"""
Database Integration Test Script
Verifies that the database is working correctly with the Flask app
"""

import os
from datetime import datetime

def test_database_connection():
    """Test database connection and data integrity"""
    print("🔍 Testing Database Integration...")
    print("="*50)
    
    try:
        # Import database module
        from database import db, get_all_students, get_all_faculty, get_all_courses
        
        # Test 1: Database file exists
        if os.path.exists('waldorf_university.db'):
            file_size = os.path.getsize('waldorf_university.db') / 1024
            print(f"✅ Database file exists: {file_size:.1f} KB")
        else:
            print("❌ Database file not found!")
            return False
        
        # Test 2: Load students
        students = get_all_students()
        print(f"✅ Students loaded: {len(students)} records")
        if students:
            print(f"   Sample: {students[0]['first_name']} {students[0]['last_name']}")
        
        # Test 3: Load faculty
        faculty = get_all_faculty()
        print(f"✅ Faculty loaded: {len(faculty)} records")
        if faculty:
            print(f"   Sample: {faculty[0]['first_name']} {faculty[0]['last_name']}")
        
        # Test 4: Load courses
        courses = get_all_courses()
        print(f"✅ Courses loaded: {len(courses)} records")
        if courses:
            print(f"   Sample: {courses[0]['course_name']}")
        
        # Test 5: Database statistics
        stats = db.get_database_stats()
        print(f"✅ Database statistics:")
        for key, value in stats.items():
            if '_count' in key:
                print(f"   {key.replace('_count', '').title()}: {value}")
        
        print("\n🎉 DATABASE INTEGRATION TEST PASSED!")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("Database integration test failed!")
        return False

def test_app_integration():
    """Test Flask app integration with database"""
    print("\n🔍 Testing Flask App Integration...")
    print("="*50)
    
    try:
        # Import app module (this will trigger database loading)
        from app import students, faculty, courses, DATABASE_AVAILABLE
        
        print(f"✅ Database available: {DATABASE_AVAILABLE}")
        print(f"✅ Students in app: {len(students)} records")
        print(f"✅ Faculty in app: {len(faculty)} records")
        print(f"✅ Courses in app: {len(courses)} records")
        
        # Check data format compatibility
        if students:
            sample_student = students[0]
            required_fields = ['id', 'name', 'major', 'year', 'gpa', 'email']
            missing_fields = [field for field in required_fields if field not in sample_student]
            
            if not missing_fields:
                print("✅ Student data format compatible")
            else:
                print(f"⚠️  Missing fields in student data: {missing_fields}")
        
        print("\n🎉 FLASK APP INTEGRATION TEST PASSED!")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("Flask app integration test failed!")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🎓 WALDORF UNIVERSITY DATABASE INTEGRATION TEST")
    print("="*60)
    print(f"  Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Run tests
    db_test = test_database_connection()
    app_test = test_app_integration()
    
    # Summary
    print("\n" + "="*60)
    if db_test and app_test:
        print("  ✅ ALL TESTS PASSED - DATABASE READY FOR USE!")
        print("="*60)
        print("  🚀 You can now start the Flask application:")
        print("     python app.py")
        print("\n  📊 Access the system at:")
        print("     http://localhost:5000")
        print("\n  🔑 Demo Login Credentials:")
        print("     Students: alice123/student123, bob456/student456")
        print("     Faculty:  prof001/faculty123, prof002/faculty456")
    else:
        print("  ❌ SOME TESTS FAILED - PLEASE CHECK ERRORS ABOVE")
    print("="*60)
    
    return db_test and app_test

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 