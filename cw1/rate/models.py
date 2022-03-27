from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    is_login = models.BooleanField()
    token = models.CharField(max_length=200)


class Professor(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)


class Course(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    semester = models.IntegerField()
    taught_by = models.ManyToManyField(to=Professor)


class Rate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'course', 'professor'),)