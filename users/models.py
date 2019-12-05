from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    isStudent_Choices = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    # add additional fields in here
    first_name = models.CharField(max_length=100, default="")
    middle_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email_address = models.CharField(max_length=100, default="")
    id_number = models.CharField(max_length=50, default="")
    isStudent = models.CharField(max_length=1,choices=isStudent_Choices, default='S', verbose_name="Student or Teacher")

    def __str__(self):
        return self.username