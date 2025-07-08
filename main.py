#!/usr/bin/env python3
"""
Waldorf Colleges and Universities Management System
Main application entry point with admin privilege testing
"""

import os
import sys
import platform
import ctypes


def check_admin_privileges():
    """Check if the application is running with admin privileges"""
    try:
        if platform.system() == "Windows":
            # Check if running as admin on Windows
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            return bool(is_admin)
        else:
            # Check if running as root on Unix-like systems
            return os.geteuid() == 0
    except:
        return False


def display_banner():
    """Display application banner"""
    print("=" * 60)
    print("    WALDORF COLLEGES AND UNIVERSITIES MANAGEMENT SYSTEM")
    print("=" * 60)
    print()


def display_admin_status():
    """Display current admin privilege status"""
    is_admin = check_admin_privileges()
    print(f"Admin Privileges: {'✓ ENABLED' if is_admin else '✗ DISABLED'}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Current User: {os.getlogin()}")
    print()
    
    if not is_admin:
        print("⚠️  WARNING: Some administrative functions may be restricted.")
        print("   Consider running as administrator for full functionality.")
        print()


def show_main_menu():
    """Display main application menu"""
    print("MAIN MENU:")
    print("1. Student Management")
    print("2. Faculty Management")
    print("3. Course Management")
    print("4. Administrative Tools (Admin Only)")
    print("5. System Settings (Admin Only)")
    print("6. Test Admin Features")
    print("0. Exit")
    print()


def student_management():
    """Student management module"""
    print("\n--- STUDENT MANAGEMENT ---")
    print("1. View Students")
    print("2. Add Student")
    print("3. Edit Student")
    print("4. Delete Student (Admin Only)")
    print("0. Back to Main Menu")
    
    choice = input("\nSelect option: ").strip()
    if choice == "1":
        print("📚 Viewing students... (Demo)")
        print("- John Doe (ID: 001)")
        print("- Jane Smith (ID: 002)")
        print("- Bob Johnson (ID: 003)")
    elif choice == "2":
        print("➕ Adding new student... (Demo)")
        name = input("Enter student name: ")
        print(f"✓ Student '{name}' added successfully!")
    elif choice == "4":
        if check_admin_privileges():
            print("🗑️ Admin function: Delete student (Demo)")
            print("✓ Student deletion functionality available")
        else:
            print("❌ Access Denied: Admin privileges required")
    

def test_admin_features():
    """Test admin-specific features"""
    print("\n--- ADMIN PRIVILEGE TEST ---")
    is_admin = check_admin_privileges()
    
    print(f"Current privilege level: {'ADMINISTRATOR' if is_admin else 'STANDARD USER'}")
    print()
    
    # Test file system access
    try:
        test_path = "admin_test.txt"
        with open(test_path, "w") as f:
            f.write("Admin test file")
        print("✓ File creation: PASSED")
        os.remove(test_path)
        print("✓ File deletion: PASSED")
    except PermissionError:
        print("❌ File operations: FAILED (Permission denied)")
    except Exception as e:
        print(f"❌ File operations: FAILED ({str(e)})")
    
    # Test admin-only functions
    if is_admin:
        print("✓ Admin menu access: AVAILABLE")
        print("✓ System configuration: AVAILABLE")
        print("✓ User management: AVAILABLE")
    else:
        print("⚠️ Admin menu access: RESTRICTED")
        print("⚠️ System configuration: RESTRICTED")
        print("⚠️ User management: RESTRICTED")


def main():
    """Main application loop"""
    display_banner()
    display_admin_status()
    
    while True:
        show_main_menu()
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            student_management()
        elif choice == "2":
            print("\n--- FACULTY MANAGEMENT ---")
            print("Faculty management module (Demo)")
        elif choice == "3":
            print("\n--- COURSE MANAGEMENT ---")
            print("Course management module (Demo)")
        elif choice == "4":
            if check_admin_privileges():
                print("\n--- ADMINISTRATIVE TOOLS ---")
                print("Administrative tools available (Demo)")
            else:
                print("\n❌ Access Denied: Administrator privileges required")
        elif choice == "5":
            if check_admin_privileges():
                print("\n--- SYSTEM SETTINGS ---")
                print("System settings available (Demo)")
            else:
                print("\n❌ Access Denied: Administrator privileges required")
        elif choice == "6":
            test_admin_features()
        elif choice == "0":
            print("\nExiting Waldorf Colleges and Universities Management System...")
            print("Thank you for using our system!")
            sys.exit(0)
        else:
            print("\n❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1) 