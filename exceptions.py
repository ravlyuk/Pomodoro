class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Incorrect password"

class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.detail = f"User with username '{username}' already exists"