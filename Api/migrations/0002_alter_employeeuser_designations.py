# Generated by Django 4.0.5 on 2022-06-27 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='designations',
            field=models.CharField(choices=[('SOFTWARE ENGINEER', 'Software Engineer'), ('TRAINEE ENGINEER', 'Trainee Engineer'), ('ASSOCIATE SOFTWARE ENGINEER', 'Associate Software Engineer')], max_length=40),
        ),
    ]
