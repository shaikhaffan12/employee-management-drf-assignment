# Generated by Django 4.0.5 on 2022-06-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_alter_employeeuser_designations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeuser',
            name='designations',
            field=models.CharField(choices=[('SOFTWARE ENGINEER', 'Software Engineer'), ('ASSOCIATE SOFTWARE ENGINEER', 'Associate Software Engineer'), ('TRAINEE ENGINEER', 'Trainee Engineer')], max_length=40),
        ),
    ]
