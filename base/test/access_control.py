from functools import wraps

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = kwargs.get('role', 'guest')  # Simulating user role
            if user_role != required_role:
                return "Access Denied!"
            return func(*args, **kwargs)
        return wrapper
    return decorator

@role_required("admin")
def delete_user(role):
    return "User Deleted!"

print(delete_user(role="admin"))
print(delete_user(role="user"))