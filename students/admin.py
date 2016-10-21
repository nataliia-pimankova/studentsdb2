from django.contrib import admin
from .models.Student import Student
from .models.Group import Group
from .models.Test import Test

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Test)
