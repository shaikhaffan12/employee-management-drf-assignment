from django.urls import path
from Api import views 

urlpatterns = [
    path('createaccount/',views.CreateApi.as_view(),name='createaccount'),
    path('login/',views.UserLogin.as_view(),name='login'),  
    path('profile/',views.UserProfile.as_view(),name='profile'),   
    path('createadmin',views.CreateSuperUser.as_view(),name='createadmin'),
    path('createmanager',views.CreateManager.as_view(),name='createmanager'),
    path('forget/', views.forget_password.as_view(), name='Forget Password'),
    path('logout/', views.UserLogout.as_view(), name='User Logout'),
]