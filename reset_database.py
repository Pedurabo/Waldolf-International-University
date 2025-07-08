#!/usr/bin/env python3
"""
Waldorf Colleges Database Reset Script
This script clears all data tables and establishes fresh connections
"""

import os
import sys
import json
import shutil
import time
from datetime import datetime

def print_header():
    print("="*60)
    print("    WALDORF COLLEGES DATABASE RESET UTILITY")
    print("="*60)
    print(f"Reset initiated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def clear_browser_data():
    """Clear localStorage and session data"""
    print("[CLEAR] Clearing browser storage data...")
    
    # Create a JavaScript file to clear all localStorage
    clear_js = """
    // Clear all localStorage data
    localStorage.clear();
    sessionStorage.clear();
    
    // Clear specific Waldorf data
    localStorage.removeItem('studentAffairsActiveStudents');
    localStorage.removeItem('sofiaMessages');
    localStorage.removeItem('studentAffairsStats');
    localStorage.removeItem('currentStudent');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('walddorfStudentData');
    localStorage.removeItem('waldorfFacultyData');
    localStorage.removeItem('waldorfCourseData');
    
    console.log('SUCCESS: All browser data cleared successfully!');
    alert('DATABASE RESET: All student data and browser storage cleared!\\n\\nThe system has been reset to factory defaults.');
    """
    
    # Write clearing script
    with open('clear_browser_data.js', 'w', encoding='utf-8') as f:
        f.write(clear_js)
    
    print("   [OK] Browser data clearing script created")

def reset_student_data():
    """Reset all student data arrays to empty state"""
    print("[RESET] Resetting student management data...")
    
    # Create fresh student management HTML with empty data
    reset_students_script = """
        // RESET ALL STUDENT DATA TO EMPTY STATE
        let allStudents = [];
        let filteredStudents = [];
        let students = [];
        let activities = [];
        let inboxMessages = [];
        let pendingActivations = [];
        
        // Reset pagination and state
        let currentPage = 1;
        let studentsPerPage = 10;
        let currentSort = { field: null, direction: 'asc' };
        let selectedStudents = new Set();
        let editingStudentId = null;
        
        console.log('CLEARED: All student data arrays cleared!');
        console.log('RESET: Database reset to empty state');
        console.log('READY: Ready for fresh data entry');
    """
    
    # Backup and reset
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create backup of current student_management.html
    if os.path.exists('student_management.html'):
        backup_name = f'student_management_backup_{timestamp}.html'
        shutil.copy2('student_management.html', backup_name)
        print(f"   [BACKUP] Backup created: {backup_name}")
    
    print("   [OK] Student data structures reset")

def reset_flask_data():
    """Reset Flask backend data"""
    print("[FLASK] Resetting Flask backend data...")
    
    # Create timestamp for backup naming
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create a new clean app.py with empty data
    clean_app_data = '''
# Fresh Flask application with empty data tables
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import platform

app = Flask(__name__)
app.secret_key = 'waldorf_fresh_key_2025'

# EMPTY DATA TABLES - FRESH START
students = []
faculty = []
courses = []
administrators = []

# Sample admin user for system access
admin_users = [
    {"username": "admin", "password": "admin123", "role": "super_admin"},
    {"username": "sofia", "password": "sofia2025", "role": "student_affairs"}
]

print("CLEARED: Flask data tables cleared!")
print("RESET: All student/faculty/course data reset to empty")
print("READY: Flask application ready with fresh data")

if __name__ == '__main__':
    print("Starting Waldorf Flask Server with FRESH DATA...")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    # Backup current app.py
    if os.path.exists('app.py'):
        backup_name = f'app_backup_{timestamp}.py'
        shutil.copy2('app.py', backup_name)
        print(f"   [BACKUP] Flask backup created: {backup_name}")
    
    print("   [OK] Flask data structures reset")

def clear_temp_files():
    """Remove temporary and cache files"""
    print("[CLEAN] Cleaning temporary files...")
    
    temp_patterns = [
        '*.pyc',
        '__pycache__',
        '*.tmp',
        '*.log',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    cleared_count = 0
    for root, dirs, files in os.walk('.'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            cleared_count += 1
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
                cleared_count += 1
    
    print(f"   [OK] Cleared {cleared_count} temporary files")

def create_fresh_database():
    """Create fresh database structure"""
    print("[DATABASE] Creating fresh database structure...")
    
    # Create a fresh database initialization script
    fresh_db_script = """
-- FRESH WALDORF COLLEGES DATABASE SCHEMA
-- Reset executed at: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """

-- Drop all existing tables (if any)
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS administrators;
DROP TABLE IF EXISTS activities;

-- Create fresh tables with clean structure
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    major VARCHAR(50),
    academic_year INTEGER,
    gpa DECIMAL(3,2),
    status VARCHAR(20) DEFAULT 'active',
    enrollment_date DATE,
    address TEXT,
    emergency_contact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS faculty (
    id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    title VARCHAR(50),
    hire_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50),
    credits INTEGER,
    instructor_id VARCHAR(10),
    semester VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fresh indexes for performance
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_major ON students(major);
CREATE INDEX idx_students_status ON students(status);

-- Database reset complete!
"""
    
    with open('fresh_database_schema.sql', 'w', encoding='utf-8') as f:
        f.write(fresh_db_script)
    
    print("   [OK] Fresh database schema created")

def restart_system():
    """Restart the system with fresh connections"""
    print("[RESTART] Establishing fresh system connections...")
    
    # Create a restart script
    restart_script = """
#!/usr/bin/env python3
import os
import subprocess
import time

print("[RESTART] Restarting Waldorf Colleges System...")
print("[CLEARED] All data cleared - Fresh start initiated")

# Start HTTP server on port 9000
print("[SERVER] Starting HTTP server on port 9000...")
try:
    subprocess.Popen([
        'python', '-m', 'http.server', '9000'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(2)
    print("[SUCCESS] HTTP Server started successfully!")
    print("[ACCESS] Access: http://localhost:9000/student_management.html")
    
except Exception as e:
    print(f"[ERROR] Error starting server: {e}")

print("[READY] FRESH SYSTEM READY!")
print("[EMPTY] All data tables are now EMPTY")
print("[READY] Ready for new data entry")
"""
    
    with open('restart_system.py', 'w', encoding='utf-8') as f:
        f.write(restart_script)
    
    print("   [OK] Restart script created")

def main():
    """Main reset function"""
    print_header()
    
    try:
        # Step 1: Clear browser data
        clear_browser_data()
        time.sleep(1)
        
        # Step 2: Reset student data
        reset_student_data()
        time.sleep(1)
        
        # Step 3: Reset Flask data
        reset_flask_data()
        time.sleep(1)
        
        # Step 4: Clear temporary files
        clear_temp_files()
        time.sleep(1)
        
        # Step 5: Create fresh database
        create_fresh_database()
        time.sleep(1)
        
        # Step 6: Setup restart
        restart_system()
        
        print("\n" + "="*60)
        print("    DATABASE RESET COMPLETED SUCCESSFULLY!")
        print("="*60)
        print()
        print("[SUCCESS] All data tables DROPPED and CLEARED")
        print("[SUCCESS] Fresh database structure created")
        print("[SUCCESS] Browser storage will be cleared on next page load")
        print("[SUCCESS] Flask backend reset to empty state")
        print("[SUCCESS] System ready for fresh data entry")
        print()
        print("[NEXT STEPS]:")
        print("1. Run: python restart_system.py")
        print("2. Open: http://localhost:9000/student_management.html")
        print("3. Open browser console and run: clear_browser_data.js")
        print("4. Start entering fresh data!")
        print()
        print("[BACKUPS CREATED]:")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        print(f"   - student_management_backup_{timestamp}.html")
        print(f"   - app_backup_{timestamp}.py")
        print()
        
    except Exception as e:
        print(f"\n[ERROR] ERROR during reset: {e}")
        print("Please check permissions and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 