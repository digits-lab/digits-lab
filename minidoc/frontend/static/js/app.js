document.addEventListener('DOMContentLoaded', () => {
    const doctorList = document.getElementById('doctor-list');
    const searchInput = document.getElementById('doctor-search');
    let doctors = [];

    // Fetch doctors from the API
    fetch('/api/doctors')
        .then(response => response.json())
        .then(data => {
            doctors = data;
            displayDoctors(doctors);
        });

    // Display doctors in the UI
    function displayDoctors(doctorsToDisplay) {
        doctorList.innerHTML = '';
        doctorsToDisplay.forEach(doctor => {
            const doctorCard = `
                <div class="bg-white p-4 rounded-lg shadow">
                    <h3 class="text-xl font-bold">${doctor.name}</h3>
                    <p class="text-gray-600">${doctor.specialization}</p>
                    <p class="text-gray-600">${doctor.contact}</p>
                    <p class="text-gray-600">Availability: ${doctor.availability}</p>
                    <p class="text-gray-600">Hospital ID: ${doctor.hospital_id}</p>
                    <button class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" onclick="openBookingModal(${doctor.id})">Book Appointment</button>
                </div>
            `;
            doctorList.innerHTML += doctorCard;
        });
    }

    // Filter doctors based on search input
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredDoctors = doctors.filter(doctor =>
            doctor.name.toLowerCase().includes(searchTerm) ||
            doctor.specialization.toLowerCase().includes(searchTerm)
        );
        displayDoctors(filteredDoctors);
    });

    const hospitalList = document.getElementById('hospital-list');

    // Fetch hospitals from the API
    fetch('/api/hospitals')
        .then(response => response.json())
        .then(data => {
            displayHospitals(data);
        });

    // Display hospitals in the UI
    function displayHospitals(hospitals) {
        hospitalList.innerHTML = '';
        hospitals.forEach(hospital => {
            const hospitalCard = `
                <div class="bg-white p-4 rounded-lg shadow">
                    <h3 class="text-xl font-bold">${hospital.name}</h3>
                    <p class="text-gray-600">Available Beds: ${hospital.available_beds}</p>
                    <p class="text-gray-600">Total Beds: ${hospital.total_beds}</p>
                    <p class="text-gray-600">Cost Index: ${hospital.cost_index}</p>
                </div>
            `;
            hospitalList.innerHTML += hospitalCard;
        });
    }
});

const bookingModal = document.getElementById('booking-modal');
const bookingForm = document.getElementById('booking-form');
const doctorIdInput = document.getElementById('doctor-id-input');

function openBookingModal(doctorId) {
    doctorIdInput.value = doctorId;
    bookingModal.classList.remove('hidden');
}

function closeBookingModal() {
    bookingModal.classList.add('hidden');
}

bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const appointmentData = {
        doctor_id: doctorIdInput.value,
        patient_id: document.getElementById('patient-id').value,
        date_time: document.getElementById('date-time').value,
        reason: document.getElementById('reason').value,
        is_urgent: document.getElementById('is-urgent').checked
    };

    fetch('/api/appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(appointmentData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeBookingModal();
    });
});

const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

loginBtn.addEventListener('click', () => loginModal.classList.remove('hidden'));
registerBtn.addEventListener('click', () => registerModal.classList.remove('hidden'));

function closeLoginModal() {
    loginModal.classList.add('hidden');
}

function closeRegisterModal() {
    registerModal.classList.add('hidden');
}

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const loginData = {
        email: document.getElementById('login-email').value,
        password: document.getElementById('login-password').value
    };

    fetch('/api/patients/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.patient_id) {
            localStorage.setItem('patient_id', data.patient_id);
            window.location.href = '/patient_portal';
        } else {
            alert(data.message);
        }
    });
});

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const registerData = {
        name: document.getElementById('register-name').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value
    };

    fetch('/api/patients/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registerData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        closeRegisterModal();
    });
});

const aiDiagnoseForm = document.getElementById('ai-diagnose-form');
const diagnosisResult = document.getElementById('diagnosis-result');

aiDiagnoseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const symptoms = document.getElementById('symptoms').value;
    diagnosisResult.innerHTML = '<p>Loading...</p>';

    fetch('/api/ai_diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms })
    })
    .then(response => response.json())
    .then(data => {
        if (data.diagnosis) {
            diagnosisResult.innerHTML = `<p><strong>Diagnosis:</strong> ${data.diagnosis}</p>`;
        } else {
            diagnosisResult.innerHTML = `<p class="text-red-500">Error: ${data.error}</p>`;
        }
    });
});