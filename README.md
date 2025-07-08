# 🎓 Waldorf Colleges & Universities Management System

A comprehensive web-based management system for educational institutions built with Flask and modern web technologies.

## 📋 Features

### 🏠 Main Dashboard
- System overview and statistics
- Real-time status monitoring
- Quick access to all modules
- Admin privilege detection

### 👥 Student Management
- View all enrolled students
- Add new students with detailed information
- Search and filter students
- Track academic progress (GPA, year, major)

### 👨‍🏫 Faculty Management
- Faculty member directory
- Department-wise organization
- Faculty information management
- Search functionality

### 🔧 Admin Panel
- Administrative control panel
- System management tools
- User management
- Database administration
- Security monitoring
- Emergency controls

### 📊 API Endpoints
- `/api/status` - System status and health check
- Real-time system monitoring
- JSON responses for integration

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager
- Windows 10+ (for admin privilege features)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/waldorf-management-system.git
cd waldorf-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌐 Available URLs

| URL | Description |
|-----|-------------|
| `/` | Main Dashboard (Home) |
| `/students` | Student Management |
| `/faculty` | Faculty Management |
| `/admin` | Admin Panel (requires admin privileges) |
| `/add_student` | Add New Student Form |
| `/admin/test` | Admin Testing Page |
| `/api/status` | System Status API |

## 🎯 Usage

### For Regular Users:
1. Navigate to `http://localhost:5000`
2. Use the main dashboard to access student and faculty management
3. Add new students through the dedicated form
4. Search and manage existing records

### For Administrators:
1. Access the admin panel at `http://localhost:5000/admin`
2. Use advanced system management tools
3. Monitor system performance and security
4. Manage user permissions and database operations

## 🛡️ Security Features

- Admin privilege detection and validation
- Secure session management
- Input validation and sanitization
- Role-based access control
- System monitoring and logging

## 🏗️ Project Structure

```
waldorf-management-system/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
├── templates/                     # HTML templates
│   ├── dashboard.html             # Main dashboard
│   ├── students.html              # Student management
│   ├── faculty.html               # Faculty management
│   ├── add_student.html           # Add student form
│   ├── admin.html                 # Admin panel
│   ├── student_home.html          # Student portal
│   └── student_login.html         # Student login
├── venv/                          # Virtual environment (excluded from git)
└── other project files...
```

## 📊 Sample Data

The application comes with pre-loaded sample data:

### Students:
- Alice Johnson (Computer Science, Junior, GPA: 3.8)
- Bob Smith (Mathematics, Senior, GPA: 3.6)
- Carol Davis (Physics, Freshman, GPA: 3.9)
- David Wilson (Chemistry, Senior, GPA: 3.7)

### Faculty:
- Dr. Sarah Johnson (Computer Science, Professor)
- Dr. Michael Brown (Mathematics, Associate Professor)
- Dr. Emily Davis (Physics, Assistant Professor)

## 🔧 Technical Details

### Built With:
- **Backend:** Python Flask 3.1.1
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Modern CSS with gradients and animations
- **Database:** In-memory data structures (expandable to SQL databases)
- **Security:** Windows admin privilege integration

### Key Components:
- Responsive web design
- Real-time status monitoring
- Advanced search functionality
- Modern UI with smooth animations
- Cross-platform compatibility

## 🌟 Features in Detail

### Dashboard
- Live system statistics
- Quick action buttons
- Navigation to all modules
- Admin status indicator

### Student Management
- Comprehensive student profiles
- Academic tracking
- Search and filter capabilities
- Form validation

### Faculty Management
- Department organization
- Faculty profiles with avatars
- Search functionality
- Status tracking

### Admin Panel
- System management tools
- Database administration
- Security monitoring
- Emergency controls
- Performance statistics

## 🚀 Development

### Running in Development Mode
The application runs in debug mode by default, providing:
- Auto-reload on file changes
- Detailed error messages
- Debug toolbar
- Console logging

### Admin Privileges
- The application detects Windows admin privileges
- Admin features are enabled/disabled based on user permissions
- Fallback options for non-admin users

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation
- Review the code comments for implementation details

## 🎯 Future Enhancements

- Database integration (SQLite/PostgreSQL)
- User authentication and authorization
- Course management system
- Grade tracking and reporting
- Email notifications
- API documentation with Swagger
- Mobile responsive improvements
- Multi-language support

---

**Made with ❤️ for Educational Institution Management** 