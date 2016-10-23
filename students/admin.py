from django.contrib import admin
from .models.Student import Student
from .models.Group import Group
from .models.Test import Test
from .models.Result import Result

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Test)
admin.site.register(Result)
