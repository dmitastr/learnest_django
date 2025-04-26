from django.contrib import admin
from django.urls import include, path
from base import views

app_name = "base"

urlpatterns = [
    path('grid/', views.GridPage.as_view()),
    path('', views.HomePage.as_view(), name="home"),

    #     path('student/<int:student_id>/', views.student_page, name="student_page"),
    path('student/<int:student_id>/',
         views.StudentPageView.as_view(), name="student_page"),


    path(r'^student/add/$', views.add_student, {}, name='add_student'),
    path('student/edit/<int:student_id>/',
         views.add_student, name='edit_student'),
    path('student/delete/<int:student_id>/',
         views.delete_student, name='delete_student'),
    path('student/<int:student_id>/add_purchase/',
         views.purchase_add, name="purchase_add"),

    path('package/all', views.package_list, name="package_list"),
    path('package/add', views.package_add, name="package_add"),
    path('package/edit/<int:package_id>',
         views.package_add, name="package_edit"),
    path('package/delete/<int:package_id>',
         views.package_delete, name="package_delete"),

    path('purchase/<int:purchase_id>/spent_lessons_increment',
         views.spent_lesson_increment, name="spent_lessons_increment"),


]
