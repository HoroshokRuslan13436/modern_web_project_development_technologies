import requests
import json

BASE_URL = "http://localhost:5000"


def send_request(method, endpoint, data=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        elif method == "GET":
            response = requests.get(url, params=params)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, json=data)
        else:
            print("Unsupported method.")
            return None

        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error: {response.status_code}, Message: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def create_patient():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-05-15",
        "gender": "Male",
        "phone_number": "1234567890"
    }
    patient = send_request("POST", "/patients", data)
    if patient:
        print(f"Patient created: {json.dumps(patient, indent=2)}")
        return patient.get('id')
    return None


def update_patient(patient_id):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-05-15",
        "gender": "Male",
        "phone_number": "0987654321"
    }
    patient = send_request("PUT", f"/patients/{patient_id}", data)
    if patient:
        print(f"Patient updated: {json.dumps(patient, indent=2)}")


def delete_patient(patient_id):
    result = send_request("DELETE", f"/patients/{patient_id}")
    if result:
        print(f"Patient with ID {patient_id} deleted.")


def create_doctor():
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "specialty": "Cardiology",
        "phone_number": "0987654321"
    }
    doctor = send_request("POST", "/doctors", data)
    if doctor:
        print(f"Doctor created: {json.dumps(doctor, indent=2)}")
        return doctor.get('id')
    return None


def update_doctor(doctor_id):
    data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "specialty": "Cardiology",
        "phone_number": "0987654321"
    }
    doctor = send_request("PUT", f"/doctors/{doctor_id}", data)
    if doctor:
        print(f"Doctor updated: {json.dumps(doctor, indent=2)}")


def delete_doctor(doctor_id):
    result = send_request("DELETE", f"/doctors/{doctor_id}")
    if result:
        print(f"Doctor with ID {doctor_id} deleted.")


def create_appointment(patient_id, doctor_id, appointment_date, appointment_time):
    data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time
    }
    appointment = send_request("POST", "/appointments", data)
    if appointment:
        print(f"Appointment created: {json.dumps(appointment, indent=2)}")


def update_appointment(appointment_id):
    data = {
        "appointment_date": "2025-06-01",
        "appointment_time": "14:00:00"
    }
    appointment = send_request("PUT", f"/appointments/{appointment_id}", data)
    if appointment:
        print(f"Appointment updated: {json.dumps(appointment, indent=2)}")


def delete_appointment(appointment_id):
    result = send_request("DELETE", f"/appointments/{appointment_id}")
    if result:
        print(f"Appointment with ID {appointment_id} deleted.")


def get_appointments(page=1, per_page=5):
    params = {"page": page, "per_page": per_page}
    appointments = send_request("GET", "/appointments", params=params)
    if appointments:
        print(f"Page {page} - Appointments:")
        print(json.dumps(appointments, indent=2))


def main():
    patient_id = create_patient()
    doctor_id = create_doctor()

    if patient_id and doctor_id:
        create_appointment(patient_id, doctor_id, "2025-05-01", "10:30:00")

    print("\nUpdating patient...")
    update_patient(patient_id)

    print("\nUpdating doctor...")
    update_doctor(doctor_id)

    print("\nUpdating appointment...")
    appointment_id = 1
    update_appointment(appointment_id)

    print("\nDeleting patient...")
    delete_patient(patient_id)

    print("\nDeleting doctor...")
    delete_doctor(doctor_id)

    print("\nDeleting appointment...")
    delete_appointment(appointment_id)

    for page in range(1, 6):
        print(f"\nFetching appointments for Page {page}:")
        get_appointments(page=page, per_page=50)


if __name__ == "__main__":
    main()
