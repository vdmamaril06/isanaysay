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
        return self.first_name + " " + self.middle_name + " " + self.last_name

class Course(models.Model):
    name = models.CharField(verbose_name="Course Name", max_length=128)
    course_code = models.CharField(verbose_name="Course Code", max_length=128)
    course_description = models.CharField(verbose_name="Course Code", max_length=500)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return "%s" % self.course_code

class Essay(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    name = models.CharField(verbose_name="Essay Name", max_length=300)
    essay_code = models.CharField(verbose_name="Essay Code", max_length=100)
    maximum_length = models.IntegerField(verbose_name="Maximum Length")
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    duration = models.IntegerField(verbose_name="Duration")

    def __str__(self):
        return "%s" % self.name

class EssaySubmission(models.Model):
    essay = models.ForeignKey(Essay, verbose_name="Essay", on_delete = models.CASCADE)
    student = models.ForeignKey(CustomUser, verbose_name="Student", on_delete = models.CASCADE)
    content = models.CharField(verbose_name="Essay Content", max_length=3000)
    submitted_date = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    essay = models.ForeignKey(Essay, verbose_name="Essay", on_delete = models.CASCADE)
    word = models.CharField(verbose_name="word", max_length=100)

    def __str__(self):
        return "%s" % self.essay

class Enrollment(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    student = models.ForeignKey(CustomUser, verbose_name="Student", on_delete = models.CASCADE)
