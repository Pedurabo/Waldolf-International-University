import platform
import ctypes
import os

# Check admin privileges
is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())

print("=" * 50)
print("WALDORF MANAGEMENT SYSTEM - ADMIN TEST")
print("=" * 50)
print(f"Admin Status: {'ENABLED' if is_admin else 'DISABLED'}")
print(f"System: {platform.system()} {platform.release()}")
print(f"User: {os.getlogin()}")
print("=" * 50)

if is_admin:
    print("✅ ALL ADMIN FEATURES ACCESSIBLE!")
    print("✅ Student Management (Full Access)")
    print("✅ Faculty Administration")
    print("✅ System Settings")
    print("✅ Administrative Tools")
    print("✅ Security Configuration")
else:
    print("⚠️ LIMITED ACCESS MODE")
    print("❌ Admin features restricted")
    
print("=" * 50) 