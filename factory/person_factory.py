from model.patient import Patient
from model.doctor import Doctor

class PersonFactory:
    _registry = {'patient': Patient, 'doctor': Doctor}

    @classmethod
    def create(cls, role, **kwargs):
        cls_ref = cls._registry.get(role)
        if cls_ref is None:
            raise ValueError(f'Невідомий тип: {role!r}')
        return cls_ref(**kwargs)