#!/usr/bin/env python3
"""
Simple Web Server for Waldorf Management System
Runs on localhost and can be accessed via Chrome
"""

import http.server
import socketserver
import webbrowser
import os
import platform
import ctypes
from urllib.parse import parse_qs


def check_admin_privileges():
    """Check admin privileges"""
    try:
        if platform.system() == "Windows":
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        else:
            return os.geteuid() == 0
    except:
        return False


class WaldorfHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/waldorf_chrome.html'
        elif self.path == '/api/status':
            self.send_api_status()
            return
        elif self.path == '/api/admin_test':
            self.send_admin_test()
            return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send_api_status(self):
        """Send system status as JSON"""
        is_admin = check_admin_privileges()
        response = f'''{{
    "status": "operational",
    "admin_privileges": {"true" if is_admin else "false"},
    "system": "{platform.system()} {platform.release()}",
    "user": "{os.getlogin()}",
    "python_version": "{platform.python_version()}",
    "features": {{
        "student_management": true,
        "faculty_management": true,
        "admin_panel": {"true" if is_admin else "false"},
        "security_settings": {"true" if is_admin else "false"}
    }}
}}'''
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())
    
    def send_admin_test(self):
        """Send admin test results"""
        is_admin = check_admin_privileges()
        
        # Test file operations
        file_test = "PASSED"
        try:
            test_file = "web_admin_test.txt"
            with open(test_file, "w") as f:
                f.write("Web admin test")
            os.remove(test_file)
        except:
            file_test = "FAILED"
        
        response = f'''{{
    "admin_status": "{'ADMINISTRATOR' if is_admin else 'STANDARD_USER'}",
    "file_operations": "{file_test}",
    "system_access": "{'AVAILABLE' if is_admin else 'RESTRICTED'}",
    "user_management": "{'AVAILABLE' if is_admin else 'RESTRICTED'}",
    "security_settings": "{'AVAILABLE' if is_admin else 'RESTRICTED'}",
    "test_timestamp": "{platform.platform()}"
}}'''
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode())


def start_server(port=8080):
    """Start the web server"""
    try:
        handler = WaldorfHandler
        httpd = socketserver.TCPServer(("", port), handler)
        
        print("=" * 60)
        print("🎓 WALDORF MANAGEMENT SYSTEM - WEB SERVER")
        print("=" * 60)
        print(f"🔑 Admin Privileges: {'✅ ENABLED' if check_admin_privileges() else '❌ DISABLED'}")
        print(f"💻 System: {platform.system()} {platform.release()}")
        print(f"👤 User: {os.getlogin()}")
        print(f"🌐 Server running on: http://localhost:{port}")
        print(f"📱 Opening in Chrome...")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Open in Chrome
        webbrowser.open(f'http://localhost:{port}')
        
        # Start server
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()
    except Exception as e:
        print(f"❌ Server error: {str(e)}")


if __name__ == "__main__":
    start_server() 