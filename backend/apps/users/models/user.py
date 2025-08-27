from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.constants import DomainException, RoleCodes
from apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise DomainException(2006)
        extra_fields.setdefault("role", RoleCodes.CLIENT)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", RoleCodes.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise DomainException(2007)
        if extra_fields.get("is_superuser") is not True:
            raise DomainException(2008)

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    role = models.CharField(
        max_length=20,
        choices=RoleCodes.choices,
        default=RoleCodes.CLIENT,
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.role}"
