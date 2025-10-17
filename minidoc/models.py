from app import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(200), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_beds = db.Column(db.Integer, nullable=False)
    occupied_beds = db.Column(db.Integer, nullable=False)
    cost_index = db.Column(db.Float, nullable=False)
    doctors = db.relationship('Doctor', backref='hospital', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) # In a real app, hash this!

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False)
    patient = db.relationship('Patient', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    refills = db.Column(db.Integer, nullable=False)
    delivery_status = db.Column(db.String(50), default='Pending')
    patient = db.relationship('Patient', backref='prescriptions', lazy=True)
    doctor = db.relationship('Doctor', backref='prescriptions', lazy=True)

class AreaStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(100), nullable=False)
    illness = db.Column(db.String(100), nullable=False)
    case_count = db.Column(db.Integer, nullable=False)