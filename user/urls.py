from django.contrib import admin
from django.urls import include, path

from user import views

app_name = "user"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name="login"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
]
