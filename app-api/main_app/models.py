from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **cargs):
        """Create and save new user"""
        if not email:
            raise ValueError('Users must have an email adress')

        user = self.model(email=self.normalize_email(email), **cargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superUser(self, email, password):
        """Create and save new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""

    email = models.EmailField(max_length=245, unique=True)
    name = models.CharField(max_length=245)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
