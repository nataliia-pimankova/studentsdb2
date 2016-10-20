from django.contrib import admin
from .models.Student import Student
from .models.Group import Group

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
