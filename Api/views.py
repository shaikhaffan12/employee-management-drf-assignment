import email
import random
from urllib import request, response
from django.shortcuts import render
from Api import serializer as ser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from Api import serializer
from Api.models import EmployeeUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,logout
from django.core.mail import send_mail
from Api.serializer import (EmployeeLoginSerializer,
                            EmployeeProfileSerializer,
                            EmployeeSerializer,
                            SuperUserSerializer,
                            ForgetPasswordSerializer)

# Create your views here.


def create_token(user): # function for jwt token creation

    user_token = RefreshToken.for_user(user= user)

    token = {
        'access' : str(user_token.access_token),
        'refresh' : str(user_token)
    }

    return token

def random_password(): # function for random password creation
    string = 'abcdefghijklmnopqrstuvxyz'
    string_upper = string.upper()
    number = '1234567890'
    special_character = '@#$%^&*!'
    combine = string + string_upper + number + special_character
    password = "".join(random.sample(combine, 6))
    return password

class forget_password(UpdateAPIView): # view for forget password
    queryset = EmployeeUser
    serializer_class = ForgetPasswordSerializer

    def send_mail(self,email,password): # Function for sending mail
        print(email,password)
        send_mail(
            'About Credntial',
            f'''Email :- {email} 
             password {password}''',
            'shaikh.affan@mindbowser.com',

            [email],
            fail_silently=False,
        )

    def update(self, request): 
        try:
            obj = EmployeeUser.objects.get(email = request.data['email']) # get email from model into variable

            password = random_password() # save random password to variable
            obj.set_password(password) 
            print('updated password', password)
            
            obj.save()
            self.send_mail(request.data['email'], password) #send mail with email and password
            # response message for successfully sending of mail
            return Response({"status":"Success", "message": "Password Reset Successfull, Updated Password Sent to Registered mail"}) 

        except BaseException as e: # if email Is not there in database then this block executes with response message
            print('Error', e)
            return response({"status": "faild", "message": "something went wrong"}, status= status.HTTP_406_NOT_ACCEPTABLE)

class CreateApi(CreateAPIView): #view for creating employees

    authentication_classes = [BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EmployeeUser
    serializer_class = EmployeeSerializer

    def send_mail(self,email,password): # sending mail function
        print(email,password)
        send_mail(
            'About Credntial',
            f'''Email :- {email} 
             password {password}''',
            'shaikh.affan@mindbowser.com',

            [email],
            fail_silently=False,
        )

   

    def post(self,request):
        user_manager = EmployeeUser.objects.get(email = request.user) # get mail form model to variable
        manager_serializer = ser.CheckManagerSerializer(user_manager) # check if it is manager
        is_manager = manager_serializer.data['is_manager'] 

        if is_manager: 
            user_data = request.data # if manager then store manager's data to variable
            serializer = EmployeeSerializer(data= user_data) # pass requested data to serializer and save it to the variable
            if serializer.is_valid():
                email = request.data.get('email') # if serializer is valid then get the mail
                serializer.save() # save the serializer
                user = EmployeeUser.objects.get(email=email)  # get email from database to variable 
                password = random_password() # create random password
                user.set_password(password) # set password
                tokenn = create_token(user)  # create token bye calling function
                user.save() # save instance 
                self.send_mail(email,password) # send mail with email and password
                return Response({"status": "success", "token": tokenn}, status=status.HTTP_200_OK)

            else: #else if there any error then respond with status
                return Response({"status": "Failed"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else: # if user is not manager then he/she not have rights to register employee or crud operataion
            return Response({"status":"failed","message":"Your Not Manager So You Have Not Rights To Register Emplyoee"})




class UserLogin(CreateAPIView): # view for login for users who already registerd

    serializer_class = EmployeeLoginSerializer
    queryset = EmployeeUser
    authentication_classes = [JWTAuthentication]
    def user_object(self,user):
        user_obj = EmployeeUser.objects.get(email=user)
        return user_obj

    def user_profile(self,user):
        profile_serializer = EmployeeProfileSerializer(user)
        return profile_serializer.data

    def post(self, request):
        serializer = EmployeeLoginSerializer(data=request.data) # store serialize data to variable
        if serializer.is_valid(raise_exception=True): 
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password) # user authenticate with email and password 
            if user is not None:
                user_obj = self.user_object(email) # get mail of user from database
                user_profile = self.user_profile(user_obj) # get profile from profile serializer with the help of email
                user_token = create_token(user_obj) # create token for user

                return Response({'status': 'login successfully','profile':user_profile,'token':user_token}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'login Failed'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'login Failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogout(RetrieveAPIView): # view for logout existing user
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,JWTAuthentication]
    serializer_class = EmployeeProfileSerializer
    queryset = EmployeeUser
    def get(self,request):
        user_profile = EmployeeProfileSerializer(request.user) # get email object from profile serializer
        token = RefreshToken(request.data.get('refresh')) # extract refresh token 
        # accessToken = RefreshToken(request.data.get('access'))
        token.blacklist() # then blacklist that token
        logout(request)
        return Response({"status":"Logged Out!","User":user_profile.data['email']})

class UserProfile(RetrieveAPIView): # view for user profile of any user

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def getUserDetail(self,user_email): # get user details
        detail = EmployeeUser.objects.get(email=user_email)
        profile_serializer = EmployeeProfileSerializer(detail)
        return profile_serializer.data

    def get(self, request):
        serializer = EmployeeProfileSerializer(request.user)
        return Response({"status":"success","profile":serializer.data}) # give response with profile data
   

class CreateSuperUser(CreateAPIView): # view for create super user
    serializer_class = SuperUserSerializer

    def setPassword(self,user,password): # passwor function superuser set password for itself
        user_obj = EmployeeUser.objects.get(email=user)
        user_obj.set_password(password)
        user_obj.save()
        return

    def post(self, request):
        try:
            super_user = EmployeeUser.objects.get(is_admin=True)
            # if the super user is already there the return this response
            return Response({"status":"Failed Super is Already There"},status=status.HTTP_406_NOT_ACCEPTABLE) 

        except BaseException as e:
            print("error",e) 

            serializer = SuperUserSerializer(data=request.data) # other wise pass data to serializer
            # print(serializer.data.get('password'))
            if serializer.is_valid(raise_exception=True):
                email = request.data['email']
                password = request.data['password']
                serializer.save()
                self.setPassword(email,password)
                return Response({"status":"success","Admin":"created"})


class CreateManager(CreateSuperUser,CreateAPIView): # view for manager
    serializer_class = ser.ManagerSerialzer
    permission_classes = [IsAdminUser]
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        try:
            manger_user = EmployeeUser.objects.get(is_manager=True)
            return Response({"status":"Failed Manager User Is Already There"},status=status.HTTP_406_NOT_ACCEPTABLE)
               
        except BaseException:
            serializer = ser.ManagerSerialzer(data=request.data)
            # print(serializer.data.get('password'))
            if serializer.is_valid(raise_exception=True):
                email = request.data['email']
                password = request.data['password']
                serializer.save()
                self.setPassword(email,password)
                return Response({"status":"success","Admin":"created"})


