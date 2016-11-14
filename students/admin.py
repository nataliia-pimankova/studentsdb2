# -*- coding: utf-8 -*-

from django.contrib import admin
from .models.Student import Student
from .models.Group import Group
from .models.Test import Test
from .models.Result import Result

from django.core.urlresolvers import reverse

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name','ticket','notes']

    def view_on_site(self,obj):
        return reverse('students_edit', kwargs={'pk':obj.id})

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Test)
admin.site.register(Result)
