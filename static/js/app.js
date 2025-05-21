// Theme Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved theme preference or use default
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
    
    // Theme toggle event listener
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            // Save preference to localStorage
            const theme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
            localStorage.setItem('theme', theme);
        });
    }
    
    // Auth form toggle (Login/Register)
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (loginTab && registerTab) {
        loginTab.addEventListener('click', function() {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            loginForm.style.display = 'block';
            registerForm.style.display = 'none';
        });
        
        registerTab.addEventListener('click', function() {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            registerForm.style.display = 'block';
            loginForm.style.display = 'none';
        });
    }
    
    // User type toggle (User/Doctor)
    const userOption = document.getElementById('user-option');
    const doctorOption = document.getElementById('doctor-option');
    const doctorFields = document.getElementById('doctor-fields');
    const userTypeInput = document.getElementById('user-type');
    
    if (userOption && doctorOption) {
        userOption.addEventListener('click', function() {
            userOption.classList.add('active');
            doctorOption.classList.remove('active');
            if (doctorFields) {
                doctorFields.style.display = 'none';
                
                // FIX: Remove required attribute from doctor fields when patient is selected
                const doctorInputs = doctorFields.querySelectorAll('input, select');
                doctorInputs.forEach(input => {
                    input.removeAttribute('required');
                });
            }
            
            if (userTypeInput) userTypeInput.value = 'user';
            // Create a hidden input for form submission
            let hiddenInput = document.querySelector('input[name="user_type"]');
            if (!hiddenInput) {
                hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'user_type';
                document.getElementById('register-form').appendChild(hiddenInput);
            }
            hiddenInput.value = 'user';
        });
        
        doctorOption.addEventListener('click', function() {
            doctorOption.classList.add('active');
            userOption.classList.remove('active');
            if (doctorFields) {
                doctorFields.style.display = 'block';
                
                // FIX: Restore required attribute for doctor fields when doctor is selected
                const doctorInputs = doctorFields.querySelectorAll('input, select');
                doctorInputs.forEach(input => {
                    if (['experience', 'fees', 'phone', 'specialization'].includes(input.name)) {
                        input.setAttribute('required', '');
                    }
                });
            }
            
            if (userTypeInput) userTypeInput.value = 'doctor';
            // Create a hidden input for form submission
            let hiddenInput = document.querySelector('input[name="user_type"]');
            if (!hiddenInput) {
                hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'user_type';
                document.getElementById('register-form').appendChild(hiddenInput);
            }
            hiddenInput.value = 'doctor';
        });
        
        // Initialize user type on page load and apply the fix immediately
        if (userOption.classList.contains('active')) {
            if (userTypeInput) userTypeInput.value = 'user';
            let hiddenInput = document.querySelector('input[name="user_type"]');
            if (!hiddenInput) {
                hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'user_type';
                document.getElementById('register-form').appendChild(hiddenInput);
            }
            hiddenInput.value = 'user';
            
            // FIX: Remove required attribute from doctor fields on initial load if patient is selected
            if (doctorFields) {
                doctorFields.style.display = 'none';
                const doctorInputs = doctorFields.querySelectorAll('input, select');
                doctorInputs.forEach(input => {
                    input.removeAttribute('required');
                });
            }
        }
    }
    
    // Appointment booking time slot selection
    const timeSlots = document.querySelectorAll('.time-slot');
    const timeInput = document.getElementById('appointment-time');
    
    if (timeSlots.length > 0) {
        timeSlots.forEach(slot => {
            slot.addEventListener('click', function() {
                // Remove selected class from all slots
                timeSlots.forEach(s => s.classList.remove('selected'));
                
                // Add selected class to clicked slot
                this.classList.add('selected');
                
                // Update hidden input value
                if (timeInput) {
                    timeInput.value = this.getAttribute('data-time');
                }
            });
        });
    }
    
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            }, 5000);
        });
    }
    
    // Initialize Google Map for contact page
    const mapContainer = document.getElementById('map');
    if (mapContainer && typeof google !== 'undefined') {
        const location = { lat: 40.7128, lng: -74.0060 }; // Default to NYC
        const map = new google.maps.Map(mapContainer, {
            zoom: 15,
            center: location
        });
        
        const marker = new google.maps.Marker({
            position: location,
            map: map,
            title: 'HealthBooker Clinic'
        });
    }
});

// AJAX for doctor search
function searchDoctors() {
    const searchTerm = document.getElementById('search-term').value;
    const specialization = document.getElementById('specialization').value;
    
    fetch(`/search-doctors?term=${searchTerm}&specialization=${specialization}`)
        .then(response => response.json())
        .then(data => {
            const doctorsList = document.getElementById('doctors-list');
            doctorsList.innerHTML = '';
            
            if (data.length === 0) {
                doctorsList.innerHTML = '<div class="col-12"><p class="text-center">No doctors found matching your criteria.</p></div>';
                return;
            }
            
            data.forEach(doctor => {
                const doctorCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card doctor-card">
                            <img src="/static/images/uploads/${doctor.profile_image}" class="card-img-top" alt="${doctor.name}">
                            <div class="doctor-info">
                                <h5 class="doctor-name">${doctor.name}</h5>
                                <div class="doctor-specialization">${doctor.specialization}</div>
                                <div class="doctor-details">
                                    <p><i class="fas fa-briefcase"></i> ${doctor.experience} years experience</p>
                                    <p><i class="fas fa-money-bill-wave"></i> ₹${doctor.fees}</p>
                                    <p><i class="fas fa-phone"></i> ${doctor.phone}</p>
                                </div>
                                <a href="/book-appointment/${doctor.id}" class="btn btn-primary btn-block">Book Appointment</a>
                            </div>
                        </div>
                    </div>
                `;
                doctorsList.innerHTML += doctorCard;
            });
        })
        .catch(error => {
            console.error('Error searching doctors:', error);
        });
}

// Update appointment status (for doctors)
function updateAppointmentStatus(appointmentId, status) {
    fetch('/update-appointment-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            appointment_id: appointmentId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Get the appointment row
            const appointmentRow = document.querySelector(`tr[data-appointment-id="${appointmentId}"]`);
            if (appointmentRow) {
                // Update status badge
                const statusBadge = appointmentRow.querySelector(`#status-${appointmentId}`);
                if (statusBadge) {
                    statusBadge.textContent = status;
                    statusBadge.className = `badge badge-${status.toLowerCase().replace(' ', '-')}`;
                }

                // Get the target tab content based on status
                const targetTabId = status.toLowerCase().replace(' ', '-');
                const targetTabContent = document.getElementById(targetTabId);
                const sourceTabContent = appointmentRow.closest('.tab-pane');

                if (targetTabContent && sourceTabContent) {
                    // Move the row to the target tab's table
                    const targetTableBody = targetTabContent.querySelector('tbody');
                    if (targetTableBody) {
                        targetTableBody.appendChild(appointmentRow);
                    }

                    // Update the actions buttons based on the new status
                    const actionsCell = appointmentRow.querySelector('td:last-child');
                    if (actionsCell) {
                        if (status === 'In Progress') {
                            actionsCell.innerHTML = `
                                <div class="btn-group">
                                    <button class="btn btn-sm btn-success" onclick="updateAppointmentStatus(${appointmentId}, 'Completed')">
                                        Complete
                                    </button>
                                    <button class="btn btn-sm btn-danger" onclick="updateAppointmentStatus(${appointmentId}, 'Cancelled')">
                                        Cancel
                                    </button>
                                </div>
                            `;
                        } else if (status === 'Completed' || status === 'Cancelled') {
                            actionsCell.innerHTML = ''; // Remove action buttons for completed/cancelled appointments
                        }
                    }

                    // Check if the source tab is now empty
                    const sourceTableBody = sourceTabContent.querySelector('tbody');
                    if (sourceTableBody && sourceTableBody.children.length === 0) {
                        // Show the "no appointments" message
                        sourceTabContent.innerHTML = `
                            <div class="text-center py-5">
                                <i class="fas fa-clipboard-check fa-4x text-muted mb-3"></i>
                                <h3>No ${sourceTabContent.id.replace('-', ' ')} appointments</h3>
                                <p>You don't have any ${sourceTabContent.id.replace('-', ' ')} appointments at the moment.</p>
                            </div>
                        `;
                    }

                    // Switch to the target tab
                    const targetTab = document.querySelector(`button[data-bs-target="#${targetTabId}"]`);
                    if (targetTab) {
                        const tab = new bootstrap.Tab(targetTab);
                        tab.show();
                    }
                }
            }
            
            // Show success message
            const alertContainer = document.getElementById('alert-container');
            if (alertContainer) {
                alertContainer.innerHTML = `
                    <div class="alert alert-success fade-in">
                        Appointment status updated successfully to ${status}.
                    </div>
                `;
                
                // Auto-dismiss alert
                setTimeout(() => {
                    alertContainer.querySelector('.alert').style.opacity = '0';
                    setTimeout(() => {
                        alertContainer.innerHTML = '';
                    }, 500);
                }, 5000);
            }
        }
    })
    .catch(error => {
        console.error('Error updating appointment status:', error);
        // Show error message
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            alertContainer.innerHTML = `
                <div class="alert alert-danger fade-in">
                    Error updating appointment status. Please try again.
                </div>
            `;
        }
    });
}
