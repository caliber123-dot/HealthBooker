from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField, HiddenField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = HiddenField('User Type', default='user')
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class DoctorForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[
        ('Cardiology', 'Cardiology (Heart)'),
        ('Ophthalmology', 'Ophthalmology (Eye)'),
        ('Orthopedics', 'Orthopedics (Bones/Joints)'),
        ('Neurology', 'Neurology (Brain/Nerves)'),
        ('Pediatrics', 'Pediatrics (Children)'),
        ('Dermatology', 'Dermatology (Skin)'),
        ('MBBS', 'MBBS (General Medicine)'),
        ('BDS', 'BDS (Dentistry)'),
        ('BAMS', 'BAMS (Ayurveda)')
    ])
    experience = IntegerField('Years of Experience', validators=[DataRequired()])
    fees = FloatField('Consultation Fees (₹)', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])

class UpdateProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')

class UpdateDoctorForm(FlaskForm):
    specialization = SelectField('Specialization', choices=[
        ('Cardiology', 'Cardiology (Heart)'),
        ('Ophthalmology', 'Ophthalmology (Eye)'),
        ('Orthopedics', 'Orthopedics (Bones/Joints)'),
        ('Neurology', 'Neurology (Brain/Nerves)'),
        ('Pediatrics', 'Pediatrics (Children)'),
        ('Dermatology', 'Dermatology (Skin)'),
        ('MBBS', 'MBBS (General Medicine)'),
        ('BDS', 'BDS (Dentistry)'),
        ('BAMS', 'BAMS (Ayurveda)')
    ])
    experience = IntegerField('Years of Experience', validators=[DataRequired()])
    fees = FloatField('Consultation Fees (₹)', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Update')

class AppointmentForm(FlaskForm):
    date = DateField('Appointment Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Appointment Time', validators=[DataRequired()], format='%H:%M')
    submit = SubmitField('Book Appointment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
