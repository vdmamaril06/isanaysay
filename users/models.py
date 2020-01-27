from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    pass
    isStudent_Choices = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    # add additional fields in here
    first_name = models.CharField(verbose_name="First Name", max_length=100, default="")
    middle_name = models.CharField(verbose_name="Middle Name", max_length=100, default="")
    last_name = models.CharField(verbose_name="Last Name", max_length=100, default="")
    email_address = models.CharField(verbose_name="Email Address", max_length=100, default="some@email.com")
    id_number = models.CharField(verbose_name="ID Number", max_length=50, default="")
    isStudent = models.CharField(max_length=1,choices=isStudent_Choices, default='S', verbose_name="Student or Teacher")

    def __str__(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

class Course(models.Model):
    pass
    semester_Choices = (
        ('A', 'First Semester'),
        ('B', 'Second Semester'),
        ('C', 'Summer'),
    )
    shoolYear_Choices = (
        ('1', '2019-2020'),
        ('2', '2020-2021'),
        ('3', '2021-2022'),
    )
    name = models.CharField(verbose_name="Course Name", max_length=128)
    course_code = models.CharField(verbose_name="Course Code", max_length=128)
    course_description = models.CharField(verbose_name="Course Description", max_length=500)
    course_detail = models.CharField(verbose_name="Course Detail", max_length=100)
    course_semester = models.CharField(max_length=1,choices=semester_Choices, default='A', verbose_name="Semester")
    course_school_year = models.CharField(max_length=1,choices=shoolYear_Choices, default='20', verbose_name="School Year")
    start_date = models.DateField(verbose_name="Course Start Date")
    end_date = models.DateField(verbose_name="Course End Date")

    def __str__(self):
        return "%s" % self.course_code

class Essay(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    name = models.CharField(verbose_name="Essay Name", max_length=300)
    essay_description = models.CharField(verbose_name="Essay Description", max_length=1500)
    essay_code = models.CharField(verbose_name="Essay Code", max_length=100)
    maximum_length = models.IntegerField(verbose_name="Maximum Length")
    start_date_time = models.DateTimeField(verbose_name="Essay Start Date")
    end_date_time = models.DateTimeField(verbose_name="Essay End Date")
    duration = models.IntegerField(verbose_name="Duration")

    def __str__(self):
        return "%s" % self.name

class EssaySubmission(models.Model):
    pass
    isChecked_Choices = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    essay = models.ForeignKey(Essay, verbose_name="Essay", on_delete = models.CASCADE)
    student = models.ForeignKey(CustomUser, verbose_name="Student", on_delete = models.CASCADE)
    content = models.CharField(verbose_name="Essay Content", max_length=3000)
    isChecked = models.CharField(max_length=1,choices=isChecked_Choices, default='N', verbose_name="Checked or Not Checked")
    submitted_date = models.DateTimeField(verbose_name="Essay Submission Date", auto_now_add=True)
    grammar_score = models.FloatField(verbose_name="Grammar Score", default=0)
    spelling_score = models.FloatField(verbose_name="Spelling Score", default=0)
    content_score = models.FloatField(verbose_name="Content Score", default=0)
    ambiguity_score = models.FloatField(verbose_name="Ambiguity Score", default=0)

class Word(models.Model):
    essay = models.ForeignKey(Essay, verbose_name="Essay", on_delete = models.CASCADE)
    word = models.CharField(verbose_name="Word", max_length=100)
    weight = models.FloatField(verbose_name="Weight", default=0)

    def __str__(self):
        return "%s" % self.essay

class Criterion(models.Model):
    essay = models.ForeignKey(Essay, verbose_name="Essay", on_delete = models.CASCADE)
    name = models.CharField(verbose_name="Criterion Name", max_length=100)
    description = models.CharField(verbose_name="Criterion Description", max_length=300)
    percentage = models.FloatField(verbose_name="Percentage")

    def __str__(self):
        return "%s" % self.essay

class Score(models.Model):
    essaySubmission = models.ForeignKey(EssaySubmission, verbose_name="Essay Submission", on_delete = models.CASCADE)
    criterion = models.ForeignKey(Criterion, verbose_name="Criterion", on_delete = models.CASCADE)
    score = models.FloatField(verbose_name="Raw Score")

    def __str__(self):
        return "%s" % self.essaySubmission

class Enrollment(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    student = models.ForeignKey(CustomUser, verbose_name="Student", on_delete = models.CASCADE)

    def __str__(self):
        return "%s" % self.course

class Assignment(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    teacher = models.ForeignKey(CustomUser, verbose_name="Teacher", on_delete = models.CASCADE)

    def __str__(self):
        return "%s" % self.course
