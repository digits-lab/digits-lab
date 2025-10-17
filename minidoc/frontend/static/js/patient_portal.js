document.addEventListener('DOMContentLoaded', () => {
    const appointmentsList = document.getElementById('appointments-list');
    const prescriptionsList = document.getElementById('prescriptions-list');
    const logoutBtn = document.getElementById('logout-btn');

    const patientId = localStorage.getItem('patient_id');

    if (!patientId) {
        window.location.href = '/';
        return;
    }

    // Fetch appointments
    fetch(`/api/patients/${patientId}/appointments`)
        .then(response => response.json())
        .then(data => {
            displayAppointments(data);
        });

    // Fetch prescriptions
    fetch(`/api/patients/${patientId}/prescriptions`)
        .then(response => response.json())
        .then(data => {
            displayPrescriptions(data);
        });

    function displayAppointments(appointments) {
        appointmentsList.innerHTML = '';
        appointments.forEach(app => {
            const appointmentItem = `
                <div class="border p-4 rounded-lg">
                    <p><strong>Doctor:</strong> ${app.doctor_name}</p>
                    <p><strong>Date:</strong> ${new Date(app.date_time).toLocaleString()}</p>
                    <p><strong>Reason:</strong> ${app.reason}</p>
                    ${app.is_urgent ? '<p class="text-red-500 font-bold">Urgent</p>' : ''}
                </div>
            `;
            appointmentsList.innerHTML += appointmentItem;
        });
    }

    function displayPrescriptions(prescriptions) {
        prescriptionsList.innerHTML = '';
        prescriptions.forEach(p => {
            const prescriptionItem = `
                <div class="border p-4 rounded-lg">
                    <p><strong>Doctor:</strong> ${p.doctor_name}</p>
                    <p><strong>Medication:</strong> ${p.medication}</p>
                    <p><strong>Dosage:</strong> ${p.dosage}</p>
                    <p><strong>Refills:</strong> ${p.refills}</p>
                    <p><strong>Status:</strong> ${p.delivery_status}</p>
                </div>
            `;
            prescriptionsList.innerHTML += prescriptionItem;
        });
    }

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('patient_id');
        window.location.href = '/';
    });
});