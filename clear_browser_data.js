
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
    alert('DATABASE RESET: All student data and browser storage cleared!\n\nThe system has been reset to factory defaults.');
    