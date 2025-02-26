from typing import Optional


class LoginDTO:
    def __init__(self, username: Optional[str] = None,
                 password: Optional[str] = None):
        self.username = username
        self.password = password

    def validate(self):
        if not all([self.username, self.password]):
            raise Exception("Username and password are required.")
        return self

    def __repr__(self):
        return f"LoginDTO(username={self.username!r}, password={self.password!r})"
