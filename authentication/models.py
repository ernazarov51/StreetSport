from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField


class User(AbstractUser):
    class RoleChoices(TextChoices):
        admin = 'admin', 'ADMIN'
        manager = 'manager', 'MANAGER'
        owner = 'owner', 'OWNER'
        user = 'user', 'USER'
    role = CharField(max_length=20,choices=RoleChoices.choices, default=RoleChoices.user)
