from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import pytz
from datetime import date
from django.utils.timezone import now

utc=pytz.UTC

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
    course_unit = models.IntegerField(verbose_name="Course Units", default=3)
    course_semester = models.CharField(max_length=1,choices=semester_Choices, default='A', verbose_name="Semester")
    course_school_year = models.CharField(max_length=1,choices=shoolYear_Choices, default='20', verbose_name="School Year")
    start_date = models.DateField(verbose_name="Course Start Date")
    end_date = models.DateField(verbose_name="Course End Date")
    students = models.ManyToManyField(CustomUser, related_name='students_enrolled')
    teacher = models.ForeignKey(CustomUser, verbose_name="Teacher", on_delete = models.CASCADE)

    def __str__(self):
        return "%s" % self.course_code

class Essay(models.Model):
    course = models.ForeignKey(Course, verbose_name="Course", on_delete = models.CASCADE)
    name = models.CharField(verbose_name="Essay Name", max_length=300)
    essay_description = models.CharField(verbose_name="Essay Description", max_length=1500)
    essay_code = models.CharField(verbose_name="Essay Code", max_length=100)
    maximum_length = models.IntegerField(verbose_name="Maximum Length")
    start_date_time = models.DateTimeField(verbose_name="Essay Start Date and Time")
    end_date_time = models.DateTimeField(verbose_name="Essay End Date and Time")
    criteria_no_1 = models.FloatField(verbose_name="Grammar",default=0)
    criteria_no_2 = models.FloatField(verbose_name="Spelling",default=0)
    criteria_no_3 = models.FloatField(verbose_name="Content",default=0)
    words = models.CharField(verbose_name="Words",max_length=10000,default="")

    def __str__(self):
        return "%s" % self.name

    def is_past_due(self):
        date_today = datetime.datetime.now().replace(tzinfo=utc)
        essay_end_date = self.end_date_time.replace(tzinfo=utc)
        return date_today > essay_end_date

    def is_ongoing(self):
        date_today = datetime.datetime.now().replace(tzinfo=utc)
        essay_end_date = self.end_date_time.replace(tzinfo=utc)
        essay_start_date = self.start_date_time.replace(tzinfo=utc)
        return date_today > essay_start_date and date_today < essay_end_date

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
    checked_date = models.DateTimeField(verbose_name="Essay Checked Date", auto_now_add=True)
    grammar_score = models.FloatField(verbose_name="Grammar Score", default=0)
    spelling_score = models.FloatField(verbose_name="Spelling Score", default=0)
    content_score = models.FloatField(verbose_name="Content Score", default=0)

    def __str__(self):
        return "%s" % self.essay

    def checked_submission(self):
        if self.isChecked == 'N':
            return False
        return True

    def get_total_score(self):
        return (self.grammar_score  * self.essay.criteria_no_1 / 100) + (self.spelling_score * self.essay.criteria_no_2 / 100 ) + (self.content_score * self.essay.criteria_no_3 / 100 )