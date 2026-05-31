from .person import Person

class Patient(Person):
    def __init__(self, person_id=None, name=None, contact=None, disease=None, diagnosis=None, age=None, gender=None, **kwargs):
        
        actual_id = person_id if person_id is not None else kwargs.get('id')
        
        super().__init__(actual_id, name, contact)
        
        self.age = age
        self.gender = gender
        self.patient_id = actual_id
        self.disease = diagnosis if diagnosis is not None else disease

    def get_info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "contact": self._contact,
            "disease": self.disease,
            "role": "patient"
        }

    @staticmethod
    def assign_doctor(cursor, conn, patient_id, doctor_id):
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()

        cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()

        if patient and doctor:
            query = "UPDATE patients SET assigned_doctor_id = %s WHERE patient_id = %s"
            cursor.execute(query, (doctor_id, patient_id))
            conn.commit()
            print(f"Doctor with ID {doctor_id} assigned to patient {patient_id}.")
        else:
            print("Patient or Doctor not found.")

    def save_to_db(self, cursor, conn):
        query = "INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)"
        values = (self.name, self.age, self.gender, self.disease)
        cursor.execute(query, values)
        conn.commit()

    @staticmethod
    def delete_from_db(cursor, conn, patient_id):
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            conn.commit()
            print(f"Patient with ID {patient_id} deleted.")
        else:
            print("Patient ID not found.")