"""Excepciones personalizadas de la aplicación"""

from fastapi import HTTPException, status


class AppException(Exception):
    """Excepción base de la aplicación"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    """Recurso no encontrado"""

    def __init__(self, resource: str, resource_id: int = None):
        message = f"{resource} no encontrado"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    """No autorizado"""

    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """Acceso prohibido"""

    def __init__(self, message: str = "Acceso prohibido"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class BadRequestException(AppException):
    """Solicitud inválida"""

    def __init__(self, message: str = "Solicitud inválida"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ConflictException(AppException):
    """Conflicto - recurso ya existe"""

    def __init__(self, message: str = "El recurso ya existe"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class ValidationException(AppException):
    """Error de validación"""

    def __init__(self, message: str = "Error de validación"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)
