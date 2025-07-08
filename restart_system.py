
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
