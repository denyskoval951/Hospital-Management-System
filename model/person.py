# Person CLass

from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, person_id, name, contact):
        self._id = person_id
        self._name = name
        self._contact = contact

    @property
    def id(self): return self._id

    @property
    def name(self): return self._name

    @abstractmethod
    def get_info(self) -> dict: ...