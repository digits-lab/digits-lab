import os
import sys
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from minidoc.app import app, db
from minidoc.models import Doctor, Hospital, Patient, Appointment, Prescription, AreaStats

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add Hospitals
        h1 = Hospital(name='General Hospital', total_beds=200, occupied_beds=150, cost_index=1.2)
        h2 = Hospital(name='City Clinic', total_beds=100, occupied_beds=80, cost_index=1.5)
        db.session.add_all([h1, h2])
        db.session.commit()

        # Add Doctors
        d1 = Doctor(name='Dr. Smith', specialization='Cardiology', contact='555-0101', availability='Mon-Fri 9am-5pm', hospital_id=h1.id)
        d2 = Doctor(name='Dr. Jones', specialization='Neurology', contact='555-0102', availability='Tue-Sat 10am-6pm', hospital_id=h1.id)
        d3 = Doctor(name='Dr. Williams', specialization='Pediatrics', contact='555-0103', availability='Mon-Wed 8am-4pm', hospital_id=h2.id)
        db.session.add_all([d1, d2, d3])
        db.session.commit()

        # Add Patients
        p1 = Patient(name='John Doe', email='john.doe@example.com', password='password')
        p2 = Patient(name='Jane Roe', email='jane.roe@example.com', password='password')
        db.session.add_all([p1, p2])
        db.session.commit()

        # Add Appointments
        a1 = Appointment(patient_id=p1.id, doctor_id=d1.id, date_time=datetime(2024, 1, 20, 10, 30), reason='Chest pain', is_urgent=True)
        a2 = Appointment(patient_id=p2.id, doctor_id=d2.id, date_time=datetime(2024, 1, 22, 14, 0), reason='Headache')
        db.session.add_all([a1, a2])
        db.session.commit()

        # Add Prescriptions
        pres1 = Prescription(patient_id=p1.id, doctor_id=d1.id, medication='Aspirin', dosage='100mg', refills=3)
        pres2 = Prescription(patient_id=p2.id, doctor_id=d2.id, medication='Tylenol', dosage='500mg', refills=1)
        db.session.add_all([pres1, pres2])
        db.session.commit()

        # Add Area Stats
        as1 = AreaStats(area='North', illness='Flu', case_count=120)
        as2 = AreaStats(area='South', illness='COVID-19', case_count=80)
        db.session.add_all([as1, as2])
        db.session.commit()

        print('Database seeded successfully!')

if __name__ == '__main__':
    seed_data()