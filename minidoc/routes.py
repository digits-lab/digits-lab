from flask import request, jsonify, render_template
from app import app, db
from models import Doctor, Hospital, Patient, Appointment, Prescription, AreaStats
import openai

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patient_portal')
def patient_portal():
    return render_template('patient_portal.html')

# Doctor Routes
@app.route('/api/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    new_doctor = Doctor(
        name=data['name'],
        specialization=data['specialization'],
        contact=data['contact'],
        availability=data['availability'],
        hospital_id=data['hospital_id']
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor created successfully'}), 201

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        'id': doc.id,
        'name': doc.name,
        'specialization': doc.specialization,
        'contact': doc.contact,
        'availability': doc.availability,
        'hospital_id': doc.hospital_id
    } for doc in doctors])

@app.route('/api/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return jsonify({
        'id': doctor.id,
        'name': doctor.name,
        'specialization': doctor.specialization,
        'contact': doctor.contact,
        'availability': doctor.availability,
        'hospital_id': doctor.hospital_id
    })

@app.route('/api/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    data = request.get_json()
    doctor.name = data['name']
    doctor.specialization = data['specialization']
    doctor.contact = data['contact']
    doctor.availability = data['availability']
    doctor.hospital_id = data['hospital_id']
    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully'})

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'})

# Hospital Routes
@app.route('/api/hospitals', methods=['POST'])
def create_hospital():
    data = request.get_json()
    new_hospital = Hospital(
        name=data['name'],
        total_beds=data['total_beds'],
        occupied_beds=data['occupied_beds'],
        cost_index=data['cost_index']
    )
    db.session.add(new_hospital)
    db.session.commit()
    return jsonify({'message': 'Hospital created successfully'}), 201

@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = Hospital.query.all()
    return jsonify([{
        'id': h.id,
        'name': h.name,
        'total_beds': h.total_beds,
        'occupied_beds': h.occupied_beds,
        'available_beds': h.total_beds - h.occupied_beds,
        'cost_index': h.cost_index
    } for h in hospitals])

@app.route('/api/hospitals/<int:id>', methods=['GET'])
def get_hospital(id):
    hospital = Hospital.query.get_or_404(id)
    return jsonify({
        'id': hospital.id,
        'name': hospital.name,
        'total_beds': hospital.total_beds,
        'occupied_beds': hospital.occupied_beds,
        'available_beds': hospital.total_beds - hospital.occupied_beds,
        'cost_index': hospital.cost_index
    })

@app.route('/api/hospitals/<int:id>', methods=['PUT'])
def update_hospital(id):
    hospital = Hospital.query.get_or_404(id)
    data = request.get_json()
    hospital.name = data['name']
    hospital.total_beds = data['total_beds']
    hospital.occupied_beds = data['occupied_beds']
    hospital.cost_index = data['cost_index']
    db.session.commit()
    return jsonify({'message': 'Hospital updated successfully'})

@app.route('/api/hospitals/<int:id>', methods=['DELETE'])
def delete_hospital(id):
    hospital = Hospital.query.get_or_404(id)
    db.session.delete(hospital)
    db.session.commit()
    return jsonify({'message': 'Hospital deleted successfully'})

# Patient Routes
@app.route('/api/patients/register', methods=['POST'])
def register_patient():
    data = request.get_json()
    # In a real app, hash the password!
    new_patient = Patient(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient registered successfully'}), 201

@app.route('/api/patients/login', methods=['POST'])
def login_patient():
    data = request.get_json()
    patient = Patient.query.filter_by(email=data['email']).first()
    if patient and patient.password == data['password']: # In a real app, check hashed password
        return jsonify({'message': 'Login successful', 'patient_id': patient.id})
    return jsonify({'message': 'Invalid credentials'}), 401

# Appointment Routes
@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        date_time=data['date_time'],
        reason=data['reason'],
        is_urgent=data.get('is_urgent', False)
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully'}), 201

@app.route('/api/patients/<int:patient_id>/appointments', methods=['GET'])
def get_patient_appointments(patient_id):
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    return jsonify([{
        'id': app.id,
        'doctor_name': app.doctor.name,
        'date_time': app.date_time,
        'reason': app.reason,
        'is_urgent': app.is_urgent
    } for app in appointments])

# Prescription Routes
@app.route('/api/prescriptions', methods=['POST'])
def issue_prescription():
    data = request.get_json()
    new_prescription = Prescription(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        medication=data['medication'],
        dosage=data['dosage'],
        refills=data['refills']
    )
    db.session.add(new_prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription issued successfully'}), 201

@app.route('/api/patients/<int:patient_id>/prescriptions', methods=['GET'])
def get_patient_prescriptions(patient_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    return jsonify([{
        'id': p.id,
        'doctor_name': p.doctor.name,
        'medication': p.medication,
        'dosage': p.dosage,
        'refills': p.refills,
        'delivery_status': p.delivery_status
    } for p in prescriptions])

# Area Stats Routes
@app.route('/api/area_stats', methods=['GET'])
def get_area_stats():
    stats = AreaStats.query.all()
    return jsonify([{
        'area': s.area,
        'illness': s.illness,
        'case_count': s.case_count
    } for s in stats])

# AI Diagnose Route
# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/api/ai_diagnose', methods=['POST'])
def ai_diagnose():
    data = request.get_json()
    symptoms = data.get('symptoms', '')

    if not symptoms:
        return jsonify({'error': 'Symptoms are required'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Diagnose the following symptoms: {symptoms}",
            max_tokens=150
        )
        diagnosis = response.choices[0].text.strip()
        return jsonify({'diagnosis': diagnosis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500