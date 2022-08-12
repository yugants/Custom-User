'''User model'''

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    '''Manager for users'''

    def create_user(self, username, password=None, role='employee', **extra_fields):
        '''Create, save and return a new user'''

        if not username:
            raise ValueError('Username must be uniquely given.')

        user = self.model(username=username, role=role, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, role='admin'):
        '''Create and return a new superuser'''

        user = self.create_user(username, password, role)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system'''

    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=30)
    is_staff = False
    is_active = True

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Tiket(models.Model):
    '''ticket table'''

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='open')
    priority = models.CharField(max_length=50, default='low')
    assignedTo = models.CharField(max_length=100)
    createdAt = models.TimeField(default=timezone.now)
