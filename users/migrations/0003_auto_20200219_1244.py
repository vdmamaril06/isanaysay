# Generated by Django 2.2 on 2020-02-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200217_0614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='duration',
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='checked_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Essay Checked Date'),
        ),
    ]