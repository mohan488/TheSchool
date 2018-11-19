from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    is_principal = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Question(models.Model):
    text = models.CharField('Question', max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return self.text


