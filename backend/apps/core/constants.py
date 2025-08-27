from django.db import models

from apps.core.utils.exceptions import DomainException


class ErrorLanguageTypes:
    """
    Defines the languages that can be used for error messages.
    """

    UZ = "uz"
    RU = "ru"


# class RoleCodes:


class ErrorTypes:
    """
    Defines different types of errors that the system may encounter.
    """

    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"
    DOMAIN_ERROR = "domain_error"


class IconTypes:
    """
    Defines different types of icons for user interface notifications.
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ConstraintNames:
    def __init__(self, exc, constraint_name):
        self.exc = exc
        self.constraint_name = constraint_name

    UNIQUE_USERNAME_FOR_USERS = "users_user_username_key"
    UNIQUE_PHONE_FOR_USERS = "users_user_phone_key"

    CONSTRAINT_EXCEPTIONS = {
        UNIQUE_USERNAME_FOR_USERS: DomainException(2004),
        UNIQUE_PHONE_FOR_USERS: DomainException(2006),
    }

    def get_exception_class(self):
        for constraint, exception in self.CONSTRAINT_EXCEPTIONS.items():
            if self.constraint_name and self.constraint_name in constraint:
                return exception
        return None


class CardChoices(models.TextChoices):
    NEW = "new", "Yangi"
    FAILED = "failed", "Muvaffaqiyatsiz"
    APPROVED = "approved", "Tasdiqlangan"
    DELIVERED = "delivered", "Yetkazib berildi"


class RoleCodes(models.TextChoices):
    ADMIN = "admin"
    CLIENT = "client"
    WORKER = "worker"
