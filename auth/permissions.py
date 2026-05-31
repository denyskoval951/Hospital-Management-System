from functools import wraps
from auth.auth_service import Role

_current_role = None

def set_session_role(role):
    global _current_role
    _current_role = role

def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if _current_role not in allowed_roles:
                raise PermissionError(
                    f'Роль {_current_role} не має доступу до {func.__name__}'
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator