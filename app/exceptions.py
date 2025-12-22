class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Incorrect password"


class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.detail = f"User with username '{username}' already exists"


class TokenExpiredException(Exception):
    detail = "Token has expired"


class TokenNotCorrectException(Exception):
    detail = "Token is not correct"


class TaskNotFoundException(Exception):
    detail = "Task not found"
