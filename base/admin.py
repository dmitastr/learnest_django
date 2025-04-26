from django.contrib import admin

from base.models import Classroom, Lesson, Package, Purchase, Student

# admin.site.register(User)
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(Package)
admin.site.register(Purchase)
