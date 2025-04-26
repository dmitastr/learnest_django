from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from base.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic.base import View

from user.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    authentication_form = LoginUserForm
    template_name = 'user/login_register.html'
    extra_context = {'title': "Sign in", "page": "login"}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/login_register.html'
    extra_context = {'title': "Sign up", "page": "register"}


class LogoutUser(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        logout(request)
        return redirect("user:login")


def login_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    context = {"page": "login"}
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User was not found")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get("next", "base:home"))
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "user/login_register.html", context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("user:login")


def register_user(request: HttpRequest) -> HttpResponse:
    context = {"page": "register", "form": UserCreationForm()}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("base:home")
        else:
            messages.error(request, "Something went wrong during registration")

    return render(request, "user/login_register.html", context)
