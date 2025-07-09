#!/usr/bin/env python3
"""
Waldorf University Database Initialization Script
This script drops all existing data and creates a fresh database with sample data
"""

import os
import sys
from datetime import datetime
from database import reset_database_fresh, db

def print_header():
    """Print initialization header"""
    print("\n" + "="*70)
    print("  🎓 WALDORF UNIVERSITY DATABASE INITIALIZATION SYSTEM")
    print("="*70)
    print(f"  Initialization started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  This will DROP ALL existing data and create fresh tables")
    print("="*70)

def print_footer():
    """Print completion footer"""
    print("\n" + "="*70)
    print("  ✅ WALDORF UNIVERSITY DATABASE READY!")
    print("="*70)
    print("  🚀 You can now start the Flask application:")
    print("     python app.py")
    print("\n  📊 Access the system at:")
    print("     http://localhost:5000")
    print("\n  🔑 Demo Login Credentials:")
    print("     Students: alice123/student123, bob456/student456")
    print("     Faculty:  prof001/faculty123, prof002/faculty456") 
    print("     Admin:    admin/admin123, sofia/sofia2025")
    print("="*70)

def confirm_reset():
    """Ask user to confirm database reset"""
    print("\n⚠️  WARNING: This will PERMANENTLY DELETE all existing data!")
    print("   - All student records will be LOST")
    print("   - All faculty data will be LOST") 
    print("   - All course information will be LOST")
    print("   - All grades and enrollments will be LOST")
    print("\n   A backup will be created automatically.")
    
    response = input("\n❓ Are you sure you want to proceed? (type 'YES' to confirm): ")
    return response.upper() == 'YES'

def main():
    """Main initialization function"""
    print_header()
    
    # Check if database exists
    if os.path.exists('waldorf_university.db'):
        print(f"\n📁 Existing database found: waldorf_university.db")
        if not confirm_reset():
            print("\n❌ Database initialization cancelled.")
            sys.exit(0)
    else:
        print("\n📁 No existing database found. Creating fresh database...")
    
    # Perform database reset
    print("\n🔄 Starting database initialization...")
    success = reset_database_fresh()
    
    if success:
        print_footer()
        
        # Test database connection
        try:
            stats = db.get_database_stats()
            print(f"\n🔍 Database Verification:")
            total_records = sum(v for k, v in stats.items() if k.endswith('_count'))
            print(f"   Total Records Created: {total_records}")
            print(f"   Database File: {stats['database_path']}")
            print(f"   File Size: {stats.get('database_size_mb', 0)} MB")
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not verify database: {e}")
        
        return True
    else:
        print("\n❌ DATABASE INITIALIZATION FAILED!")
        print("   Please check the error messages above and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 