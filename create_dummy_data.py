from datetime import datetime, timedelta
import os
import secrets
from werkzeug.security import generate_password_hash
from app import app, db, bcrypt, User, Doctor, Appointment

def create_dummy_doctors():
    # Check if we already have doctors in the database
    existing_doctors = Doctor.query.all()
    if existing_doctors:
        print("Dummy doctors already exist in the database.")
        return
    
    # Create dummy doctor users
    doctor_data = [
        {
            'username': 'Dr.JohnSmith',
            'email': 'john.smith@healthbooker.com',
            'password': 'password123',
            'profile_image': 'doctor1.jpg',
            'specialization': 'Cardiology',
            'experience': 15,
            'fees': 150.00,
            'phone': '(555) 123-4567'
        },
        {
            'username': 'Dr.SarahJohnson',
            'email': 'sarah.johnson@healthbooker.com',
            'password': 'password123',
            'profile_image': 'doctor2.jpg',
            'specialization': 'Neurology',
            'experience': 12,
            'fees': 175.00,
            'phone': '(555) 234-5678'
        },
        {
            'username': 'Dr.MichaelPatel',
            'email': 'michael.patel@healthbooker.com',
            'password': 'password123',
            'profile_image': 'doctor3.jpg',
            'specialization': 'Pediatrics',
            'experience': 10,
            'fees': 125.00,
            'phone': '(555) 345-6789'
        },
        {
            'username': 'Dr.EmilyWong',
            'email': 'emily.wong@healthbooker.com',
            'password': 'password123',
            'profile_image': 'doctor4.jpg',
            'specialization': 'Dermatology',
            'experience': 8,
            'fees': 160.00,
            'phone': '(555) 456-7890'
        }
    ]
    
    for doctor in doctor_data:
        # Create user
        hashed_password = bcrypt.generate_password_hash(doctor['password']).decode('utf-8')
        user = User(
            username=doctor['username'],
            email=doctor['email'],
            password=hashed_password,
            user_type='doctor',
            profile_image=doctor['profile_image'],
            date_joined=datetime.utcnow()
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create doctor profile
        doctor_profile = Doctor(
            user_id=user.id,
            specialization=doctor['specialization'],
            experience=doctor['experience'],
            fees=doctor['fees'],
            phone=doctor['phone']
        )
        
        db.session.add(doctor_profile)
    
    db.session.commit()
    print("Dummy doctors created successfully!")

def create_dummy_users():
    # Check if we already have regular users in the database
    existing_users = User.query.filter_by(user_type='user').first()
    if existing_users:
        print("Dummy users already exist in the database.")
        return
    
    # Create a dummy regular user
    hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(
        username='JanePatient',
        email='jane.patient@example.com',
        password=hashed_password,
        user_type='user',
        profile_image='default.jpg',
        date_joined=datetime.utcnow()
    )
    
    db.session.add(user)
    db.session.commit()
    print("Dummy regular user created successfully!")
    
    # Create a dummy doctor user for login (separate from the display doctors)
    hashed_password = bcrypt.generate_password_hash('doctor123').decode('utf-8')
    doctor_user = User(
        username='Dr.LoginTest',
        email='doctor.login@healthbooker.com',
        password=hashed_password,
        user_type='doctor',
        profile_image='default.jpg',
        date_joined=datetime.utcnow()
    )
    
    db.session.add(doctor_user)
    db.session.commit()
    
    # Create doctor profile
    doctor_profile = Doctor(
        user_id=doctor_user.id,
        specialization='MBBS',
        experience=5,
        fees=100.00,
        phone='(555) 987-6543'
    )
    
    db.session.add(doctor_profile)
    db.session.commit()
    print("Dummy doctor login account created successfully!")
    
    print("\nLogin Credentials:")
    print("------------------")
    print("Regular User:")
    print("Username: jane.patient@example.com")
    print("Password: password123")
    print("\nDoctor:")
    print("Username: doctor.login@healthbooker.com")
    print("Password: doctor123")

if __name__ == '__main__':
    with app.app_context():
        create_dummy_doctors()
        create_dummy_users()
