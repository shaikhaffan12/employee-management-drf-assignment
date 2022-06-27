from django.contrib.auth.models import BaseUserManager

class EmployeeManager(BaseUserManager):

    def create_user(self, email, phone_no,name, password=None): #manager class for Normal user
      
        if not email:
            raise ValueError('Users must have an email address') # check if user enter valid mail id otherwise raise value error

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            phone_no = phone_no
        )
        user.is_active = True # for normal user make true for is_active
        user.set_password(password) #set password function for normal user
        user.save(using=self._db) #save instance to database
        return user

    def create_superuser(self, email, phone_no, name, password=None): # manager class for super user
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email = email,
            password=password,
            name=name,
            phone_no = phone_no
        )
        user.is_admin = True # for superuser have to set is_admin true
        user.save(using=self._db) # save instance to database
        return user


        