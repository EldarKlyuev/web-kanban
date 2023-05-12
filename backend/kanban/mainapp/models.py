from django.db import models

class User(models.Model): 

    email = models.EmailField(max_length=255, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    GENDER_CHOICES = [
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина'),
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(max_length=20, blank=False)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Company', 'Company'),
        ('Worker', 'Worker'),
    ]

    role_sys = models.CharField(max_length=20,
                                choices=ROLE_CHOICES, 
                                default=ROLE_CHOICES[1][1], 
                                null=True)

    is_enable = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

    token_verify = models.CharField(max_length=255, unique=True, null=True)
    token_verify_created_at = models.DateTimeField(auto_now_add=True, null=True)

    token_reset = models.CharField(max_length=255, unique=True, null=True)
    token_reset_created_at = models.DateTimeField(null=True)

    token_complite_signup = models.CharField(max_length=255, unique=True, null=True)
    token_complite_signup_created_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
