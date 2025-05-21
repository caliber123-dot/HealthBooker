# HealthBooker - Healthcare Appointment Platform

HealthBooker is a comprehensive healthcare platform designed to connect users with doctors and streamline the appointment booking process. The application provides a modern web interface for managing healthcare interactions with robust features for both users and doctors.

## Features

### User/Doctor Registration and Authentication
- Full signup and login functionality
- Secure access control for protected features
- Combined login/registration form with toggle button (User/Doctor)

### Doctor Listings
- Browse/search available healthcare professionals by specialization
- View detailed doctor information (photo, name, specialization, experience, fees, phone)
- Book appointments with preferred doctors

### Doctor Specializations
- Cardiology (Heart)
- Ophthalmology (Eye)
- Orthopedics (Bones/Joints)
- Neurology (Brain/Nerves)
- Pediatrics (Children)
- Dermatology (Skin)
- MBBS (General Medicine)
- BDS (Dentistry)
- BAMS (Ayurveda)

### User Appointments
- View booking history in table format
- Track appointment status (Pending/Completed/In Progress/Cancelled)

### Doctor Appointments
- View appointment list for pending treatments
- Mark appointments as completed

### User/Doctor Profiles
- Personalized dashboards
- Profile update capabilities

### Contact
- Contact information and clinic address with map
- Query submission for customer support

### Additional Features
- Light and dark theme toggle
- Responsive design with modern styling

## Technology Stack
- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript, Bootstrap, AJAX
- Database: SQLite

## Installation and Setup

1. Clone the repository
2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Access the application at `http://localhost:5000`

## Project Structure
```
Health-Book-app/
    static/
        css/main.css
        js/app.js
        images/
    templates/
        index.html
        contact.html
    app.py
    requirements.txt
    README.md
```

## License
This project is for educational purposes only.
