#!/usr/bin/env python3
"""
Automated Waldorf University Database Setup
This script automatically creates and initializes the database
"""

import os
import sys
from datetime import datetime

def main():
    """Automated database setup"""
    print("\n" + "="*70)
    print("  🔄 WALDORF UNIVERSITY - AUTOMATED DATABASE SETUP")
    print("="*70)
    print(f"  Setup started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Import and run database setup
        from database import reset_database_fresh, db
        
        print("🚀 Initializing database automatically...")
        success = reset_database_fresh()
        
        if success:
            # Get database statistics
            stats = db.get_database_stats()
            
            print("\n" + "="*70)
            print("  ✅ WALDORF UNIVERSITY DATABASE READY!")
            print("="*70)
            print(f"📊 Database Statistics:")
            for key, value in stats.items():
                if '_count' in key:
                    print(f"   {key.replace('_count', '').title()}: {value}")
            print(f"   Database Size: {stats.get('database_size_mb', 0)} MB")
            print(f"   Database File: waldorf_university.db")
            
            print("\n🔑 Demo Login Credentials:")
            print("   Students: alice123/student123, bob456/student456")
            print("   Faculty:  prof001/faculty123, prof002/faculty456") 
            print("   Admin:    admin/admin123, sofia/sofia2025")
            
            print("\n🚀 Ready to start Flask application:")
            print("   python app.py")
            print("="*70)
            
            return True
            
        else:
            print("\n❌ DATABASE SETUP FAILED!")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Please make sure all required files are present.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 