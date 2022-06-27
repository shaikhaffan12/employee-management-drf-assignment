from Api.manager import EmployeeManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class EmployeeUser (AbstractBaseUser):
    employee_role = {
        ('SOFTWARE ENGINEER','Software Engineer'),
        ('ASSOCIATE SOFTWARE ENGINEER', 'Associate Software Engineer'),
        ('TRAINEE ENGINEER', 'Trainee Engineer')
    }

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=40)
    designations = models.CharField(max_length=40, choices= employee_role)
    phone_no = models.IntegerField( blank=False, null= False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_no']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        
        return self.is_admin
