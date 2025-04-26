from django.db import models
from django.db.models import QuerySet, Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpRequest


# class User(AbstractUser):
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True)
#     email = models.EmailField(unique=True, null=True)


#     avatar = models.ImageField(null=True, default="avatar.svg")
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ["username"]

#     def __str__(self):
#         return f"{self.id} - {self.name}"

class Student(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.name}"

    def get_purchases_from_me(self, teacher_id: int) -> QuerySet:
        purchases = self.purchase_set.filter(package__teacher__id=teacher_id)
        return purchases


class Classroom(models.Model):
    students = models.ManyToManyField(Student, related_name="students")
    teacher = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.teacher.id} - {self.teacher.username} students"


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    lenth_minutes = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.lenth_minutes} mins"


class Package(models.Model):
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    lessons_count = models.IntegerField()
    price = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Purchase(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    lessons_spent = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.package}"

    def get_remaining_lessons(self) -> str:
        return f"{self.package.lessons_count - self.lessons_spent}/{self.package.lessons_count}"
