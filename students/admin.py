# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models import Student, Group, Test, Result, MonthJournal
# from .models.Group import Group
# from .models.Test import Test
# from .models.Result import Result


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is leader in any group

        If Yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name','ticket','notes']
    form = StudentFormAdmin

    def view_on_site(self,obj):
        return reverse('students_edit', kwargs={'pk':obj.id})


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """Check if student is in any group

        If Yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        students = Student.objects.filter(student_group=self.instance)
        if len(students) > 0 and self.cleaned_data['leader'] != students[0]:
            raise ValidationError(u'Студент належить до іншої групи.', code='invalid')

        return self.cleaned_data['leader']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Test)
admin.site.register(Result)
admin.site.register(MonthJournal)