import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt, User, Doctor, Appointment, Contact
from forms import LoginForm, RegistrationForm, DoctorForm, UpdateProfileForm, UpdateDoctorForm, AppointmentForm, ContactForm
from datetime import datetime, time

# Helper function to save profile pictures
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/uploads', picture_fn)
    
    # Resize image
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

# Home route
@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.user_type == 'user':
            # Get appointments ordered by date in descending order
            appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
            current_user.appointments_as_user = appointments
        elif current_user.user_type == 'doctor':
            doctor = Doctor.query.filter_by(user_id=current_user.id).first()
            if doctor:
                # Get appointments ordered by date in descending order
                doctor.appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('index.html', title='Home')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    register_form = RegistrationForm()
    doctor_form = DoctorForm()
    
    if request.method == 'POST' and 'submit' in request.form:
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth.html', title='Login', 
                          login_form=login_form, 
                          register_form=register_form,
                          doctor_form=doctor_form,
                          active_tab='login')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    register_form = RegistrationForm()
    doctor_form = DoctorForm()
    
    if request.method == 'POST':
        try:
            # Simplified registration logic
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            user_type = request.form.get('user_type', 'user')
            
            # Basic validation
            if not name or not email or not password or not confirm_password:
                flash('All fields are required.', 'danger')
                return render_template('auth.html', title='Register', 
                                      login_form=login_form, 
                                      register_form=register_form,
                                      doctor_form=doctor_form,
                                      active_tab='register')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('auth.html', title='Register', 
                                      login_form=login_form, 
                                      register_form=register_form,
                                      doctor_form=doctor_form,
                                      active_tab='register')
            
            # Check if email exists
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('That email is already registered. Please use a different one.', 'danger')
                return render_template('auth.html', title='Register', 
                                      login_form=login_form, 
                                      register_form=register_form,
                                      doctor_form=doctor_form,
                                      active_tab='register')
            
            # Create user
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Handle profile picture
            profile_image = 'default.jpg'
            if 'picture' in request.files and request.files['picture'].filename:
                profile_image = save_picture(request.files['picture'])
            
            user = User(
                name=name,
                email=email,
                password=hashed_password,
                user_type=user_type,
                profile_image=profile_image
            )
            
            db.session.add(user)
            db.session.commit()
            
            # If registering as a doctor, create doctor profile
            if user_type == 'doctor':
                try:
                    specialization = request.form.get('specialization', 'General')
                    experience = request.form.get('experience', 1)
                    fees = request.form.get('fees', 50.0)
                    phone = request.form.get('phone', '0000000000')
                    
                    doctor = Doctor(
                        user_id=user.id,
                        specialization=specialization,
                        experience=int(experience),
                        fees=float(fees),
                        phone=phone
                    )
                    db.session.add(doctor)
                    db.session.commit()
                    flash('Your doctor account has been created! You can now log in.', 'success')
                except Exception as e:
                    db.session.delete(user)
                    db.session.commit()
                    flash(f'Error creating doctor profile: {str(e)}. Please try again.', 'danger')
                    return redirect(url_for('register'))
            else:
                flash('Your account has been created! You can now log in.', 'success')
            
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration error: {str(e)}. Please try again.', 'danger')
            return render_template('auth.html', title='Register', 
                                  login_form=login_form, 
                                  register_form=register_form,
                                  doctor_form=doctor_form,
                                  active_tab='register')
    
    return render_template('auth.html', title='Register', 
                          login_form=login_form, 
                          register_form=register_form,
                          doctor_form=doctor_form,
                          active_tab='register')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    doctor_form = None
    
    # If user is a doctor, initialize doctor form
    if current_user.user_type == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        doctor_form = UpdateDoctorForm()
        
        if doctor_form.validate_on_submit() and request.form.get('update_doctor'):
            doctor.specialization = doctor_form.specialization.data
            doctor.experience = doctor_form.experience.data
            doctor.fees = doctor_form.fees.data
            doctor.phone = doctor_form.phone.data
            db.session.commit()
            flash('Your doctor profile has been updated!', 'success')
            return redirect(url_for('profile'))
        
        # Pre-populate doctor form
        if doctor and request.method == 'GET':
            doctor_form.specialization.data = doctor.specialization
            doctor_form.experience.data = doctor.experience
            doctor_form.fees.data = doctor.fees
            doctor_form.phone.data = doctor.phone
    
    if form.validate_on_submit() and request.form.get('update_profile'):
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
        
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-populate user form
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    image_file = url_for('static', filename='images/uploads/' + current_user.profile_image)
    
    return render_template('profile.html', title='Profile', 
                          image_file=image_file, 
                          form=form, 
                          doctor_form=doctor_form)

# Doctors listing route
@app.route('/doctors')
def doctors():
    doctors = Doctor.query.order_by(Doctor.id.desc()).all()
    return render_template('doctors.html', title='Doctors', doctors=doctors)

# Search doctors route (AJAX)
@app.route('/search-doctors')
def search_doctors():
    term = request.args.get('term', '')
    specialization = request.args.get('specialization', '')
    
    query = Doctor.query.join(User)
    
    if term:
        query = query.filter(User.name.ilike(f'%{term}%'))
    
    if specialization and specialization != 'All':
        query = query.filter(Doctor.specialization == specialization)
    
    doctors = query.all()
    
    result = []
    for doctor in doctors:
        result.append({
            'id': doctor.id,
            'name': doctor.user.name,
            'specialization': doctor.specialization,
            'experience': doctor.experience,
            'fees': doctor.fees,
            'phone': doctor.phone,
            'profile_image': doctor.user.profile_image
        })
    
    return jsonify(result)

# Book appointment route
@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    if current_user.user_type != 'user':
        flash('Only patients can book appointments.', 'warning')
        return redirect(url_for('doctors'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    form = AppointmentForm()
    
    if form.validate_on_submit():
        # Check if appointment already exists
        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor.id,
            appointment_date=form.date.data,
            appointment_time=form.time.data
        ).first()
        
        if existing_appointment:
            flash('This time slot is already booked. Please select another time.', 'danger')
        else:
            appointment = Appointment(
                user_id=current_user.id,
                doctor_id=doctor.id,
                appointment_date=form.date.data,
                appointment_time=form.time.data,
                status='Pending'
            )
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('user_appointments'))
    
    return render_template('book_appointment.html', title='Book Appointment', 
                          doctor=doctor, form=form)

# User appointments route
@app.route('/user-appointments')
@login_required
def user_appointments():
    if current_user.user_type != 'user':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('user_appointments.html', title='My Appointments', appointments=appointments)

# Doctor appointments route
@app.route('/doctor-appointments')
@login_required
def doctor_appointments():
    if current_user.user_type != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        flash('Doctor profile not found.', 'danger')
        return redirect(url_for('home'))
    
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('doctor_appointments.html', title='Appointments', appointments=appointments)

# Update appointment status route (AJAX)
@app.route('/update-appointment-status', methods=['POST'])
@login_required
def update_appointment_status():
    if current_user.user_type != 'doctor':
        return jsonify({'success': False, 'message': 'Access denied.'})
    
    data = request.get_json()
    appointment_id = data.get('appointment_id')
    status = data.get('status')
    
    appointment = Appointment.query.get_or_404(appointment_id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if appointment.doctor_id != doctor.id:
        return jsonify({'success': False, 'message': 'Access denied.'})
    
    appointment.status = status
    db.session.commit()
    
    # Get the updated appointment data
    patient = User.query.get(appointment.user_id)
    appointment_data = {
        'id': appointment.id,
        'patient': {
            'name': patient.name,
            'profile_image': patient.profile_image
        },
        'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
        'appointment_time': appointment.appointment_time.strftime('%H:%M'),
        'booking_date': appointment.booking_date.strftime('%Y-%m-%d'),
        'status': appointment.status
    }
    
    return jsonify({
        'success': True,
        'appointment': appointment_data
    })

# Get appointments route (AJAX)
@app.route('/get-appointments')
@login_required
def get_appointments():
    if current_user.user_type != 'doctor':
        return jsonify({'success': False, 'message': 'Access denied.'})
    
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        return jsonify({'success': False, 'message': 'Doctor profile not found.'})
    
    # Get all appointments for this doctor, ordered by date
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.appointment_date.desc()).all()
    
    # Convert appointments to JSON-serializable format
    appointments_data = []
    for appointment in appointments:
        # Get the patient's user data
        patient = User.query.get(appointment.user_id)
        if patient:
            appointment_data = {
                'id': appointment.id,
                'patient': {
                    'name': patient.name,
                    'profile_image': patient.profile_image
                },
                'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d'),
                'appointment_time': appointment.appointment_time.strftime('%H:%M'),
                'booking_date': appointment.booking_date.strftime('%Y-%m-%d'),
                'status': appointment.status
            }
            appointments_data.append(appointment_data)
    
    return jsonify(appointments_data)

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', title='Contact Us', form=form)
