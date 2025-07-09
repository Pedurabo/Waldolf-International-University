#!/usr/bin/env python3
"""
Waldorf University Database Connection Module
Handles all database operations and connections
"""

import sqlite3
import os
import json
from datetime import datetime, date
from contextlib import contextmanager
from typing import List, Dict, Optional, Any

# Database configuration
DATABASE_PATH = 'waldorf_university.db'
BACKUP_PATH = 'backups/'

class WaldorfDatabase:
    """Main database class for Waldorf University Management System"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.ensure_backup_directory()
    
    def ensure_backup_directory(self):
        """Ensure backup directory exists"""
        if not os.path.exists(BACKUP_PATH):
            os.makedirs(BACKUP_PATH)
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a SELECT query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def execute_script(self, script: str):
        """Execute a SQL script (multiple statements)"""
        with self.get_connection() as conn:
            conn.executescript(script)
            conn.commit()
    
    def drop_all_tables(self):
        """Drop all existing tables"""
        print("🗑️  Dropping all existing tables...")
        
        drop_script = """
        -- Drop all existing tables
        DROP TABLE IF EXISTS enrollments;
        DROP TABLE IF EXISTS grades;
        DROP TABLE IF EXISTS assignments;
        DROP TABLE IF EXISTS activities;
        DROP TABLE IF EXISTS announcements;
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS financial_aid;
        DROP TABLE IF EXISTS transcripts;
        DROP TABLE IF EXISTS courses;
        DROP TABLE IF EXISTS faculty;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS administrators;
        DROP TABLE IF EXISTS departments;
        DROP TABLE IF EXISTS system_logs;
        """
        
        self.execute_script(drop_script)
        print("✅ All tables dropped successfully!")
    
    def create_fresh_schema(self):
        """Create fresh database schema"""
        print("🏗️  Creating fresh database schema...")
        
        schema_script = """
        -- FRESH WALDORF UNIVERSITY DATABASE SCHEMA
        -- Created at: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
        
        -- Students table
        CREATE TABLE students (
            id VARCHAR(20) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            full_name VARCHAR(200) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(20),
            major VARCHAR(100),
            academic_year INTEGER DEFAULT 1,
            gpa DECIMAL(3,2) DEFAULT 0.00,
            status VARCHAR(20) DEFAULT 'active',
            enrollment_date DATE DEFAULT CURRENT_DATE,
            graduation_date DATE,
            address TEXT,
            emergency_contact TEXT,
            date_of_birth DATE,
            gender VARCHAR(20),
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Faculty table
        CREATE TABLE faculty (
            id VARCHAR(20) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            full_name VARCHAR(200) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(20),
            department VARCHAR(100),
            title VARCHAR(100),
            office VARCHAR(50),
            hire_date DATE,
            salary DECIMAL(10,2),
            status VARCHAR(20) DEFAULT 'active',
            specialization TEXT,
            education_background TEXT,
            research_interests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Departments table
        CREATE TABLE departments (
            id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            head_faculty_id VARCHAR(20),
            building VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(150),
            budget DECIMAL(12,2),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (head_faculty_id) REFERENCES faculty(id)
        );
        
        -- Courses table
        CREATE TABLE courses (
            id VARCHAR(20) PRIMARY KEY,
            course_name VARCHAR(200) NOT NULL,
            course_code VARCHAR(20) UNIQUE NOT NULL,
            department VARCHAR(100),
            credits INTEGER DEFAULT 3,
            instructor_id VARCHAR(20),
            semester VARCHAR(50),
            academic_year VARCHAR(10),
            schedule VARCHAR(100),
            room VARCHAR(50),
            capacity INTEGER DEFAULT 30,
            enrolled INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            description TEXT,
            prerequisites TEXT,
            learning_outcomes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (instructor_id) REFERENCES faculty(id)
        );
        
        -- Enrollments table
        CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id VARCHAR(20) NOT NULL,
            course_id VARCHAR(20) NOT NULL,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            grade VARCHAR(5),
            grade_points DECIMAL(3,2),
            status VARCHAR(20) DEFAULT 'enrolled',
            attendance_percentage DECIMAL(5,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            UNIQUE(student_id, course_id)
        );
        
        -- Assignments table
        CREATE TABLE assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id VARCHAR(20) NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            assignment_type VARCHAR(50),
            due_date DATETIME,
            total_points INTEGER DEFAULT 100,
            instructions TEXT,
            status VARCHAR(20) DEFAULT 'active',
            created_by VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (created_by) REFERENCES faculty(id)
        );
        
        -- Grades table
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id VARCHAR(20) NOT NULL,
            assignment_id INTEGER NOT NULL,
            points_earned DECIMAL(5,2),
            percentage DECIMAL(5,2),
            letter_grade VARCHAR(5),
            feedback TEXT,
            submission_date DATETIME,
            graded_date DATETIME,
            graded_by VARCHAR(20),
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (assignment_id) REFERENCES assignments(id),
            FOREIGN KEY (graded_by) REFERENCES faculty(id),
            UNIQUE(student_id, assignment_id)
        );
        
        -- Financial transactions table
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id VARCHAR(20) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            payment_type VARCHAR(50),
            description VARCHAR(200),
            transaction_date DATE DEFAULT CURRENT_DATE,
            due_date DATE,
            status VARCHAR(20) DEFAULT 'pending',
            payment_method VARCHAR(50),
            reference_number VARCHAR(100),
            semester VARCHAR(50),
            academic_year VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        
        -- Announcements table
        CREATE TABLE announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            author_id VARCHAR(20),
            target_audience VARCHAR(50),
            priority VARCHAR(20) DEFAULT 'normal',
            publish_date DATE DEFAULT CURRENT_DATE,
            expiry_date DATE,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES faculty(id)
        );
        
        -- Activities/Events table
        CREATE TABLE activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            event_type VARCHAR(50),
            start_date DATETIME,
            end_date DATETIME,
            location VARCHAR(100),
            organizer_id VARCHAR(20),
            capacity INTEGER,
            registered_count INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            registration_required BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organizer_id) REFERENCES faculty(id)
        );
        
        -- System administrators table
        CREATE TABLE administrators (
            id VARCHAR(20) PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(150),
            role VARCHAR(50) DEFAULT 'admin',
            permissions TEXT,
            last_login TIMESTAMP,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- System logs table
        CREATE TABLE system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(20),
            action VARCHAR(100),
            entity_type VARCHAR(50),
            entity_id VARCHAR(50),
            details TEXT,
            ip_address VARCHAR(45),
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for better performance
        CREATE INDEX idx_students_email ON students(email);
        CREATE INDEX idx_students_major ON students(major);
        CREATE INDEX idx_students_status ON students(status);
        CREATE INDEX idx_students_year ON students(academic_year);
        
        CREATE INDEX idx_faculty_department ON faculty(department);
        CREATE INDEX idx_faculty_email ON faculty(email);
        CREATE INDEX idx_faculty_status ON faculty(status);
        
        CREATE INDEX idx_courses_instructor ON courses(instructor_id);
        CREATE INDEX idx_courses_department ON courses(department);
        CREATE INDEX idx_courses_semester ON courses(semester);
        CREATE INDEX idx_courses_status ON courses(status);
        
        CREATE INDEX idx_enrollments_student ON enrollments(student_id);
        CREATE INDEX idx_enrollments_course ON enrollments(course_id);
        CREATE INDEX idx_enrollments_status ON enrollments(status);
        
        CREATE INDEX idx_grades_student ON grades(student_id);
        CREATE INDEX idx_grades_assignment ON grades(assignment_id);
        CREATE INDEX idx_grades_status ON grades(status);
        
        CREATE INDEX idx_payments_student ON payments(student_id);
        CREATE INDEX idx_payments_status ON payments(status);
        CREATE INDEX idx_payments_date ON payments(transaction_date);
        
        CREATE INDEX idx_announcements_audience ON announcements(target_audience);
        CREATE INDEX idx_announcements_date ON announcements(publish_date);
        CREATE INDEX idx_announcements_status ON announcements(status);
        
        CREATE INDEX idx_activities_date ON activities(start_date);
        CREATE INDEX idx_activities_organizer ON activities(organizer_id);
        CREATE INDEX idx_activities_status ON activities(status);
        
        CREATE INDEX idx_logs_user ON system_logs(user_id);
        CREATE INDEX idx_logs_timestamp ON system_logs(timestamp);
        CREATE INDEX idx_logs_action ON system_logs(action);
        """
        
        self.execute_script(schema_script)
        print("✅ Fresh database schema created successfully!")
    
    def insert_sample_data(self):
        """Insert sample data for development and testing"""
        print("📊 Inserting sample data...")
        
        # Sample students
        students_data = [
            ('alice123', 'Alice', 'Johnson', 'alice.johnson@waldorf.edu', '555-0101', 'Computer Science', 2, 3.75, 'active', '2023-09-01'),
            ('bob456', 'Bob', 'Smith', 'bob.smith@waldorf.edu', '555-0102', 'Business Administration', 3, 3.45, 'active', '2022-09-01'),
            ('charlie789', 'Charlie', 'Brown', 'charlie.brown@waldorf.edu', '555-0103', 'Engineering', 1, 3.85, 'active', '2024-09-01'),
            ('diana012', 'Diana', 'Miller', 'diana.miller@waldorf.edu', '555-0104', 'Psychology', 4, 3.92, 'active', '2021-09-01'),
            ('emma345', 'Emma', 'Davis', 'emma.davis@waldorf.edu', '555-0105', 'Biology', 2, 3.68, 'active', '2023-09-01')
        ]
        
        for student in students_data:
            self.execute_update("""
                INSERT INTO students (id, first_name, last_name, email, phone, major, academic_year, gpa, status, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, student)
        
        # Sample faculty
        faculty_data = [
            ('prof001', 'Dr. Sarah', 'Wilson', 'sarah.wilson@waldorf.edu', '555-1001', 'Computer Science', 'Professor', 'CS-201', '2015-08-15', 95000.00),
            ('prof002', 'Dr. Michael', 'Johnson', 'michael.johnson@waldorf.edu', '555-1002', 'Business', 'Associate Professor', 'BUS-101', '2018-01-10', 85000.00),
            ('prof003', 'Dr. Emily', 'Rodriguez', 'emily.rodriguez@waldorf.edu', '555-1003', 'Engineering', 'Professor', 'ENG-301', '2012-09-01', 98000.00),
            ('prof004', 'Dr. James', 'Chen', 'james.chen@waldorf.edu', '555-1004', 'Psychology', 'Assistant Professor', 'PSY-105', '2020-08-20', 75000.00),
            ('prof005', 'Dr. Lisa', 'Anderson', 'lisa.anderson@waldorf.edu', '555-1005', 'Biology', 'Professor', 'BIO-202', '2010-01-15', 92000.00)
        ]
        
        for faculty in faculty_data:
            self.execute_update("""
                INSERT INTO faculty (id, first_name, last_name, email, phone, department, title, office, hire_date, salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, faculty)
        
        # Sample courses
        courses_data = [
            ('CS101', 'Introduction to Computer Science', 'CS101', 'Computer Science', 3, 'prof001', 'Fall 2024', '2024-25', 'MWF 10:00-10:50 AM', 'CS-102', 30, 25),
            ('CS201', 'Data Structures and Algorithms', 'CS201', 'Computer Science', 4, 'prof001', 'Fall 2024', '2024-25', 'TTH 2:00-3:50 PM', 'CS-201', 25, 20),
            ('BUS101', 'Business Fundamentals', 'BUS101', 'Business', 3, 'prof002', 'Fall 2024', '2024-25', 'MWF 1:00-1:50 PM', 'BUS-101', 40, 35),
            ('ENG201', 'Engineering Mathematics', 'ENG201', 'Engineering', 4, 'prof003', 'Fall 2024', '2024-25', 'TTH 10:00-11:50 AM', 'ENG-201', 30, 28),
            ('PSY101', 'Introduction to Psychology', 'PSY101', 'Psychology', 3, 'prof004', 'Fall 2024', '2024-25', 'MWF 9:00-9:50 AM', 'PSY-101', 35, 32),
            ('BIO101', 'General Biology', 'BIO101', 'Biology', 4, 'prof005', 'Fall 2024', '2024-25', 'TTH 1:00-2:50 PM', 'BIO-201', 25, 22)
        ]
        
        for course in courses_data:
            self.execute_update("""
                INSERT INTO courses (id, course_name, course_code, department, credits, instructor_id, semester, academic_year, schedule, room, capacity, enrolled)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, course)
        
        # Sample enrollments
        enrollments_data = [
            ('alice123', 'CS101', '2024-09-01', 'A', 4.0, 'enrolled', 95.5),
            ('alice123', 'CS201', '2024-09-01', 'B+', 3.3, 'enrolled', 88.2),
            ('bob456', 'BUS101', '2024-09-01', 'A-', 3.7, 'enrolled', 92.1),
            ('charlie789', 'ENG201', '2024-09-01', 'A', 4.0, 'enrolled', 97.8),
            ('diana012', 'PSY101', '2024-09-01', 'A+', 4.0, 'enrolled', 98.5),
            ('emma345', 'BIO101', '2024-09-01', 'B+', 3.3, 'enrolled', 89.7)
        ]
        
        for enrollment in enrollments_data:
            self.execute_update("""
                INSERT INTO enrollments (student_id, course_id, enrollment_date, grade, grade_points, status, attendance_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, enrollment)
        
        # Sample administrators
        admin_data = [
            ('admin001', 'admin', 'pbkdf2:sha256:150000$xyz123', 'System', 'Administrator', 'admin@waldorf.edu', 'super_admin', 'all_permissions'),
            ('staff001', 'sofia', 'pbkdf2:sha256:150000$abc456', 'Sofia', 'Martinez', 'sofia@waldorf.edu', 'student_affairs', 'student_management')
        ]
        
        for admin in admin_data:
            self.execute_update("""
                INSERT INTO administrators (id, username, password_hash, first_name, last_name, email, role, permissions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, admin)
        
        print("✅ Sample data inserted successfully!")
    
    def backup_database(self):
        """Create a backup of the current database"""
        if not os.path.exists(self.db_path):
            print("❌ No database file to backup")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"waldorf_backup_{timestamp}.db"
        backup_path = os.path.join(BACKUP_PATH, backup_filename)
        
        # Copy database file
        import shutil
        shutil.copy2(self.db_path, backup_path)
        
        print(f"✅ Database backed up to: {backup_path}")
        return backup_path
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        stats = {}
        
        try:
            # Table counts
            tables = ['students', 'faculty', 'courses', 'enrollments', 'assignments', 'grades', 'payments', 'announcements', 'activities']
            
            for table in tables:
                try:
                    result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    stats[f"{table}_count"] = result[0]['count'] if result else 0
                except:
                    stats[f"{table}_count"] = 0
            
            # Database file size
            if os.path.exists(self.db_path):
                file_size = os.path.getsize(self.db_path)
                stats['database_size_bytes'] = file_size
                stats['database_size_mb'] = round(file_size / (1024 * 1024), 2)
            
            stats['last_updated'] = datetime.now().isoformat()
            stats['database_path'] = self.db_path
            
        except Exception as e:
            stats['error'] = str(e)
        
        return stats
    
    def log_action(self, user_id: str, action: str, entity_type: str = None, entity_id: str = None, details: str = None):
        """Log system actions"""
        try:
            self.execute_update("""
                INSERT INTO system_logs (user_id, action, entity_type, entity_id, details)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, action, entity_type, entity_id, details))
        except Exception as e:
            print(f"Warning: Failed to log action: {e}")

# Global database instance
db = WaldorfDatabase()

# Convenience functions for common operations
def get_all_students() -> List[Dict]:
    """Get all students from database"""
    return db.execute_query("SELECT * FROM students WHERE status = 'active' ORDER BY last_name, first_name")

def get_all_faculty() -> List[Dict]:
    """Get all faculty from database"""
    return db.execute_query("SELECT * FROM faculty WHERE status = 'active' ORDER BY last_name, first_name")

def get_all_courses() -> List[Dict]:
    """Get all courses from database"""
    return db.execute_query("""
        SELECT c.*, f.first_name || ' ' || f.last_name as instructor_name
        FROM courses c
        LEFT JOIN faculty f ON c.instructor_id = f.id
        WHERE c.status = 'active'
        ORDER BY c.course_code
    """)

def get_student_by_id(student_id: str) -> Optional[Dict]:
    """Get student by ID"""
    results = db.execute_query("SELECT * FROM students WHERE id = ? AND status = 'active'", (student_id,))
    return results[0] if results else None

def get_faculty_by_id(faculty_id: str) -> Optional[Dict]:
    """Get faculty by ID"""
    results = db.execute_query("SELECT * FROM faculty WHERE id = ? AND status = 'active'", (faculty_id,))
    return results[0] if results else None

def get_course_by_id(course_id: str) -> Optional[Dict]:
    """Get course by ID"""
    results = db.execute_query("""
        SELECT c.*, f.first_name || ' ' || f.last_name as instructor_name
        FROM courses c
        LEFT JOIN faculty f ON c.instructor_id = f.id
        WHERE c.id = ? AND c.status = 'active'
    """, (course_id,))
    return results[0] if results else None

def reset_database_fresh():
    """Complete database reset - drop all tables and recreate with sample data"""
    print("\n🔄 STARTING COMPLETE DATABASE RESET")
    print("="*60)
    
    try:
        # Step 1: Backup existing database
        backup_path = db.backup_database()
        
        # Step 2: Drop all tables
        db.drop_all_tables()
        
        # Step 3: Create fresh schema
        db.create_fresh_schema()
        
        # Step 4: Insert sample data
        db.insert_sample_data()
        
        # Step 5: Verify setup
        stats = db.get_database_stats()
        
        print("\n✅ DATABASE RESET COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Database Statistics:")
        for key, value in stats.items():
            if '_count' in key:
                print(f"   {key.replace('_count', '').title()}: {value}")
        print(f"   Database Size: {stats.get('database_size_mb', 0)} MB")
        if backup_path:
            print(f"   Backup Created: {backup_path}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR DURING DATABASE RESET: {e}")
        return False

if __name__ == "__main__":
    # Run database reset when script is executed directly
    reset_database_fresh() 