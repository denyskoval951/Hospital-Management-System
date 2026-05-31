from enum import Enum
import bcrypt

class Role(Enum):
    ADMIN = 'admin'
    REGISTRAR = 'registrar'
    DOCTOR = 'doctor'
    PATIENT = 'patient'

class AuthService:
    @staticmethod
    def hash_password(plain: str) -> bytes:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt())

    @staticmethod
    def verify(plain: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed)