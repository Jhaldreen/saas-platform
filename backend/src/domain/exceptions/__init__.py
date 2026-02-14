class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found"""
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class EntityAlreadyExistsError(DomainException):
    """Raised when trying to create an entity that already exists"""
    def __init__(self, entity_name: str, field: str, value: str):
        self.entity_name = entity_name
        self.field = field
        self.value = value
        super().__init__(f"{entity_name} with {field}={value} already exists")


class UnauthorizedError(DomainException):
    """Raised when user is not authorized to perform action"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)


class ValidationError(DomainException):
    """Raised when business validation fails"""
    def __init__(self, message: str):
        super().__init__(message)


class InvalidCredentialsError(DomainException):
    """Raised when credentials are invalid"""
    def __init__(self):
        super().__init__("Invalid email or password")
