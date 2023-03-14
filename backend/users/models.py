from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user' 
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User')
    ]

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True)
	
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        null=False,
        unique=True)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150)
	
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150)

    password = models.CharField(
        verbose_name='Пароль',
        max_length=150)
    
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
