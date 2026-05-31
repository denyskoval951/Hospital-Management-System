import pytest
from unittest.mock import MagicMock
from factory.person_factory import PersonFactory
from events.event_bus import EventBus
from auth.auth_service import AuthService, Role
from auth.permissions import set_session_role, require_role
from service.patient_service import PatientService
from model.patient import Patient
from model.doctor import Doctor

# --- Factory ---
def test_factory_creates_patient():
    p = PersonFactory.create('patient', person_id=1,
        name='Іван', contact='123', diagnosis='Грип', assigned_doctor_id=1)
    assert isinstance(p, Patient)

def test_factory_creates_doctor():
    d = PersonFactory.create('doctor', person_id=2,
        name='Марія', contact='456', specialization='Хірург', schedule={})
    assert isinstance(d, Doctor)

def test_factory_unknown_role_raises():
    with pytest.raises(ValueError):
        PersonFactory.create('nurse')

# --- EventBus ---
def test_event_bus_notifies_subscriber():
    handler = MagicMock()
    EventBus._listeners.clear()
    EventBus.subscribe('test_event', handler)
    EventBus.publish('test_event', {'key': 'value'})
    handler.assert_called_once_with({'key': 'value'})

# --- Auth / permissions ---
def test_require_role_blocks_wrong_role():
    set_session_role(Role.DOCTOR)
    mock_repo = MagicMock()
    service = PatientService(mock_repo)
    with pytest.raises(PermissionError):
        service.create_patient({'name': 'X', 'contact': '1',
                                'diagnosis': 'Y', 'assigned_doctor_id': 1})

def test_require_role_allows_correct_role():
    set_session_role(Role.REGISTRAR)
    mock_repo = MagicMock()
    service = PatientService(mock_repo)
    service.create_patient({'name': 'X', 'contact': '1',
                            'diagnosis': 'Y', 'assigned_doctor_id': 1})
    mock_repo.save.assert_called_once()

# --- PatientService ---
def test_create_patient_saves_to_repo():
    set_session_role(Role.REGISTRAR)
    mock_repo = MagicMock()
    service = PatientService(mock_repo)
    data = {'name': 'Іван Петренко', 'contact': '+380991234567',
            'diagnosis': 'Грип', 'assigned_doctor_id': 1}
    service.create_patient(data)
    mock_repo.save.assert_called_once()
    assert mock_repo.save.call_args[0][0].name == 'Іван Петренко'

# --- Bcrypt ---
def test_bcrypt_hash_verify():
    hashed = AuthService.hash_password('secret123')
    assert AuthService.verify('secret123', hashed) is True

def test_bcrypt_wrong_password():
    hashed = AuthService.hash_password('secret123')
    assert AuthService.verify('wrong', hashed) is False