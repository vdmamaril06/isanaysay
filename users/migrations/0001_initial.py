# Generated by Django 2.2 on 2019-12-19 07:04

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(default='', max_length=100, verbose_name='First Name')),
                ('middle_name', models.CharField(default='', max_length=100, verbose_name='Middle Name')),
                ('last_name', models.CharField(default='', max_length=100, verbose_name='Last Name')),
                ('email_address', models.CharField(default='some@email.com', max_length=100, verbose_name='Email Address')),
                ('id_number', models.CharField(default='', max_length=50, verbose_name='ID Number')),
                ('isStudent', models.CharField(choices=[('S', 'Student'), ('T', 'Teacher')], default='S', max_length=1, verbose_name='Student or Teacher')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Course Name')),
                ('course_code', models.CharField(max_length=128, verbose_name='Course Code')),
                ('course_description', models.CharField(max_length=500, verbose_name='Course Description')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Course Start Date')),
                ('end_date', models.DateField(verbose_name='Course End Date')),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Criterion Name')),
                ('description', models.CharField(max_length=300, verbose_name='Criterion Description')),
                ('percentage', models.FloatField(verbose_name='Percentage')),
            ],
        ),
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Essay Name')),
                ('essay_description', models.CharField(max_length=1500, verbose_name='Essay Description')),
                ('essay_code', models.CharField(max_length=100, verbose_name='Essay Code')),
                ('maximum_length', models.IntegerField(verbose_name='Maximum Length')),
                ('start_date_time', models.DateTimeField(verbose_name='Essay Start Date')),
                ('end_date_time', models.DateTimeField(verbose_name='Essay End Date')),
                ('duration', models.IntegerField(verbose_name='Duration')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=3000, verbose_name='Essay Content')),
                ('isChecked', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=1, verbose_name='Checked or Not Checked')),
                ('submitted_date', models.DateTimeField(auto_now_add=True, verbose_name='Essay Submission Date')),
                ('grammar_score', models.FloatField(default=0, verbose_name='Grammar Score')),
                ('spelling_score', models.FloatField(default=0, verbose_name='Spelling Score')),
                ('content_score', models.FloatField(default=0, verbose_name='Content Score')),
                ('ambiguity_score', models.FloatField(default=0, verbose_name='Ambiguity Score')),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Essay', verbose_name='Essay')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Word')),
                ('weight', models.FloatField(default=0, verbose_name='Weight')),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Essay', verbose_name='Essay')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='Raw Score')),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Criterion', verbose_name='Criterion')),
                ('essaySubmission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.EssaySubmission', verbose_name='Essay Submission')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course', verbose_name='Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.AddField(
            model_name='criterion',
            name='essay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Essay', verbose_name='Essay'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Course', verbose_name='Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Teacher')),
            ],
        ),
    ]
