from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:новий_пароль@localhost:5432/Data_Base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    appointments = db.relationship('Appointment', backref='patient_ref', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}, {self.birth_date}, {self.gender}, {self.phone_number}>"


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    appointments = db.relationship('Appointment', backref='doctor_ref', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Doctor {self.first_name} {self.last_name}, {self.specialty}>"


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)

    patient = db.relationship('Patient', backref='appointments_list', lazy=True, passive_deletes=True)
    doctor = db.relationship('Doctor', backref='appointments_list', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"<Appointment {self.id} for {self.patient.first_name} with {self.doctor.first_name} on {self.appointment_date}>"


with app.app_context():
    db.create_all()


@app.route('/patients', methods=['GET'])
def get_patients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    patients = Patient.query.paginate(page=page, per_page=per_page, error_out=False)

    result = [{
        'id': p.id,
        'first_name': p.first_name,
        'last_name': p.last_name,
        'birth_date': p.birth_date.isoformat(),
        'gender': p.gender,
        'phone_number': p.phone_number
    } for p in patients.items]
    return jsonify(result)


@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    if not all(field in data for field in ['first_name', 'last_name', 'birth_date', 'gender', 'phone_number']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_patient = Patient(**data)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({
        'id': new_patient.id,
        'first_name': new_patient.first_name,
        'last_name': new_patient.last_name,
        'birth_date': new_patient.birth_date.isoformat(),
        'gender': new_patient.gender,
        'phone_number': new_patient.phone_number
    }), 201


@app.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    data = request.get_json()
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    if not all(field in data for field in ['first_name', 'last_name', 'birth_date', 'gender', 'phone_number']):
        return jsonify({'error': 'Missing required fields'}), 400

    for key, value in data.items():
        setattr(patient, key, value)

    db.session.commit()
    return jsonify({
        'id': patient.id,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'birth_date': patient.birth_date.isoformat(),
        'gender': patient.gender,
        'phone_number': patient.phone_number
    })


@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient and related appointments deleted'}), 200


@app.route('/doctors', methods=['GET'])
def get_doctors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    doctors = Doctor.query.paginate(page=page, per_page=per_page, error_out=False)

    result = [{
        'id': d.id,
        'first_name': d.first_name,
        'last_name': d.last_name,
        'specialty': d.specialty,
        'phone_number': d.phone_number
    } for d in doctors.items]
    return jsonify(result)


@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    if not all(field in data for field in ['first_name', 'last_name', 'specialty', 'phone_number']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_doctor = Doctor(**data)
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({
        'id': new_doctor.id,
        'first_name': new_doctor.first_name,
        'last_name': new_doctor.last_name,
        'specialty': new_doctor.specialty,
        'phone_number': new_doctor.phone_number
    }), 201


@app.route('/doctors/<int:id>', methods=['PUT'])
def update_doctor(id):
    data = request.get_json()
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404

    if not all(field in data for field in ['first_name', 'last_name', 'specialty', 'phone_number']):
        return jsonify({'error': 'Missing required fields'}), 400

    for key, value in data.items():
        setattr(doctor, key, value)

    db.session.commit()
    return jsonify({
        'id': doctor.id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'specialty': doctor.specialty,
        'phone_number': doctor.phone_number
    })


@app.route('/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor and related appointments deleted'}), 200


@app.route('/appointments', methods=['GET'])
def get_appointments():
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 50, type=int)  # Default to 10 appointments per page

    appointments = Appointment.query.paginate(page=page, per_page=per_page, error_out=False)

    result = [{
        'appointment_id': appt.id,
        'patient': {
            'id': appt.patient.id,
            'first_name': appt.patient.first_name,
            'last_name': appt.patient.last_name,
            'birth_date': appt.patient.birth_date.isoformat(),
            'gender': appt.patient.gender,
            'phone_number': appt.patient.phone_number
        },
        'doctor': {
            'id': appt.doctor.id,
            'first_name': appt.doctor.first_name,
            'last_name': appt.doctor.last_name,
            'specialty': appt.doctor.specialty,
            'phone_number': appt.doctor.phone_number
        },
        'appointment_date': appt.appointment_date.isoformat(),
        'appointment_time': appt.appointment_time.strftime('%H:%M:%S')
    } for appt in appointments.items]

    return jsonify({
        'appointments': result,
        'total': appointments.total,
        'page': appointments.page,
        'pages': appointments.pages
    })


@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    if not all(field in data for field in ['patient_id', 'doctor_id', 'appointment_date', 'appointment_time']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_appointment = Appointment(**data)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({
        'appointment_id': new_appointment.id,
        'patient_id': new_appointment.patient_id,
        'doctor_id': new_appointment.doctor_id,
        'appointment_date': new_appointment.appointment_date.isoformat(),
        'appointment_time': new_appointment.appointment_time.strftime('%H:%M:%S')
    }), 201


@app.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    data = request.get_json()
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    if 'patient_id' not in data or 'doctor_id' not in data:
        return jsonify({'error': 'Patient ID and Doctor ID are required'}), 400

    patient = Patient.query.get(data['patient_id'])
    doctor = Doctor.query.get(data['doctor_id'])
    if not patient or not doctor:
        return jsonify({'error': 'Patient or Doctor not found'}), 404

    for key, value in data.items():
        setattr(appointment, key, value)

    db.session.commit()
    return jsonify({
        'appointment_id': appointment.id,
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'appointment_date': appointment.appointment_date.isoformat(),
        'appointment_time': appointment.appointment_time.strftime('%H:%M:%S')
    })


@app.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
