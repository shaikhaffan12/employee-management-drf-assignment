from dataclasses import fields
from pyexpat import model
from Api.models import EmployeeUser
from Api.manager import EmployeeManager
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['email', 'name', 'phone_no', 'designations']

class EmployeeLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    class Meta:
        model = EmployeeUser
        fields = ['email','password']

class EmployeeProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = EmployeeUser
        fields = ['email','name','phone_no','designations']


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['email','phone_no','name','password','is_admin']

class CheckManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['email','is_manager']

class ManagerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['email','name','phone_no','password','is_manager']

class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['email']