from .person import Person

class Doctor(Person):
    def __init__(self, person_id=None, name=None, contact=None, specialization=None, schedule=None, age=None, gender=None, **kwargs):
        
        actual_id = person_id if person_id is not None else kwargs.get('id')
        
        super().__init__(actual_id, name, contact)
        
        self.age = age
        self.gender = gender
        self.doctor_id = actual_id
        self.specialization = specialization
        self.schedule = schedule
        self.assigned_doctor_id = None

    def get_info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "contact": self._contact,
            "specialization": self.specialization,
            "schedule": self.schedule,
            "role": "doctor"
        }

    def save_to_db(self, cursor, conn):
        query = "INSERT INTO doctors (name, age, gender, doctor_id, specialization) VALUES (%s, %s, %s, %s, %s)"
        values = (self.name, self.age, self.gender, self.doctor_id, self.specialization)
        cursor.execute(query, values)
        conn.commit()