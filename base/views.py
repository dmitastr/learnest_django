import logging
from django.forms import BaseForm
from django.db.models import QuerySet
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from base.forms import PackageForm, PurchaseForm, StudentForm
from base.models import Classroom, Package, Purchase, Student, User


logger = logging.getLogger("base")


class AuthenticatedView(LoginRequiredMixin):
    login_url = "user:login"
    redirect_field_name = "next"


class HomePage(AuthenticatedView, ListView):
    model = Student
    context_object_name = "students"
    template_name = "base/home.html"

    def get_queryset(self) -> QuerySet:
        students = super().get_queryset().filter(students__teacher=self.request.user)
        return students

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        students = self.get_queryset()

        purchases_by_student = {}
        if students:
            purchases = Purchase.objects.filter(
                package__teacher=self.request.user, student__in=students)
            for purchase in purchases:
                purchases_by_student.setdefault(
                    purchase.student_id, []).append(purchase)

        context["purchases_by_student"] = purchases_by_student
        return context


class StudentPageView(AuthenticatedView, DetailView):
    model = Student
    template_name = "base/student_page.html"
    context_object_name = "student"

    def get_object(self):
        student_id = self.kwargs.get("student_id")
        return get_object_or_404(Student, pk=student_id)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        purchases = []
        student = self.get_object()
        if student:
            purchases = Purchase.objects.filter(
                package__teacher=self.request.user, student=student)

        purchases_by_student = {student.id: purchases}
        context["purchases_by_student"] = purchases_by_student

        return context


@login_required(login_url="user:login")
def add_student(request: HttpRequest, student_id: int = None) -> HttpResponse:
    if student_id:
        student = get_object_or_404(Student, pk=student_id)
    else:
        student = Student()
    new_student_form: BaseForm = StudentForm(
        request.POST or None, instance=student)
    if request.method == "POST" and new_student_form.is_valid():
        new_student: Student = new_student_form.save()

        classroom, is_created = Classroom.objects.get_or_create(
            teacher=request.user)
        classroom.students.add(new_student)
        classroom.save()

        return redirect("base:home")

    context = {"form": new_student_form}
    return render(request, "base/add_student.html", context)


@login_required(login_url="user:login")
def delete_student(request: HttpRequest, student_id: int = None) -> HttpResponse:
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        student.delete()
        return redirect("base:home")

    context = {"obj": student}
    return render(request, "base/delete.html", context)


@login_required(login_url="user:login")
def package_list(request: HttpRequest) -> HttpResponse:
    packages = Package.objects.filter(teacher=request.user)
    context = {"packages": packages}
    return render(request, "base/package_list.html", context)


@login_required(login_url="user:login")
def package_add(request: HttpRequest, package_id: int = None) -> HttpResponse:
    if package_id:
        package = get_object_or_404(Package, pk=package_id)
        if package.teacher != request.user:
            return HttpResponse("You are not allowed to change that package")
    else:
        package = Package()
    package_form: BaseForm = PackageForm(
        request.POST or None, instance=package)

    if request.method == "POST" and package_form.is_valid():
        package_form.save(request=request)
        return redirect("base:package_list")

    context = {"form": package_form}
    return render(request, "base/package_add.html", context)


@login_required(login_url="user:login")
def package_delete(request: HttpRequest, package_id: int = None) -> HttpResponse:
    package = get_object_or_404(Package, pk=package_id)

    if package.teacher != request.user:
        return HttpResponse("You are not allowed to change that package")

    if request.method == "POST":
        package.delete()
        return redirect("base:package_list")

    context = {"obj": package}
    return render(request, "base/delete.html", context)


@login_required(login_url="user:login")
def purchase_add(request: HttpRequest, student_id: int = None) -> HttpResponse:
    purchase = Purchase()

    if student_id:
        student = get_object_or_404(Student, pk=student_id)
        purchase.student = student

    purchase_form: BaseForm = PurchaseForm(
        request.POST or None, instance=purchase, teacher=request.user)

    if request.method == "POST" and purchase_form.is_valid():
        purchase_form.save()
        return redirect("base:home")

    context = {"form": purchase_form}
    return render(request, "base/add_purchase.html", context)


@login_required(login_url="user:login")
def spent_lesson_increment(request: HttpRequest, purchase_id: int = None) -> HttpResponse:
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    if purchase and request.method == "POST":
        increment = int(request.POST.get("increment", 0))
        purchase.lessons_spent += increment
        if 0 <= purchase.lessons_spent <= purchase.package.lessons_count:
            purchase.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


class GridPage(TemplateView):
    template_name = "base/grid_page.html"
