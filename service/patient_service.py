from factory.person_factory import PersonFactory
from events.event_bus import EventBus
from auth.permissions import require_role
from auth.auth_service import Role

class PatientService:
    def __init__(self, repository):
        self._repo = repository

    @require_role(Role.ADMIN, Role.REGISTRAR)
    def create_patient(self, data: dict):
        patient = PersonFactory.create('patient', **data)
        self._repo.save(patient)
        EventBus.publish('patient_created', data)
        return patient