import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.utils import secure_filename
import secrets
from waitress import serve

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthbooker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'uploads')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Create upload folder if it doesn't exist
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'user' or 'doctor'
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    appointments_as_user = db.relationship('Appointment', backref='patient', lazy=True, 
                                          foreign_keys='Appointment.user_id')
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.user_type}')"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)  # Years of experience
    fees = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='doctor_profile', lazy=True, 
                          foreign_keys=[user_id])
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, 
                                  foreign_keys='Appointment.doctor_id')
    
    def __repr__(self):
        return f"Doctor('{self.user.name}', '{self.specialization}', '{self.experience} years')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending/Completed/In Progress/Cancelled
    
    def __repr__(self):
        return f"Appointment(Patient: '{self.patient.name}', Doctor: '{self.doctor.user.name}', Date: '{self.appointment_date}', Status: '{self.status}')"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}', '{self.subject}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import all routes
from routes import *

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    serve(app, host="0.0.0.0", port=8000)
