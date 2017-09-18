from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from .models import Student, Group, Exam, Result, MonthJournal


class StudentAdmin(TranslationAdmin):
    list_display = ['id', 'last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name','ticket','notes']
    form = StudentFormAdmin

    def view_on_site(self,obj):
        return reverse('students_edit', kwargs={'pk':obj.id})


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """Check if student is leader in any group

        If Yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        """Check if student is in any group

        If Yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        students = Student.objects.filter(student_group=self.instance)
        if len(students) > 0 and self.cleaned_data['leader'] != students[0]:
            raise ValidationError(u'Студент належить до іншої групи.', code='invalid')

        return self.cleaned_data['leader']


class GroupAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'leader']
    # list_display_links = ['title']
    list_editable = ['title', 'leader']
    ordering = ['title']
    # list_filter = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


class ExamAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'teacher', 'date', 'group']
    list_display_links = ['title']
    list_editable = ['group', 'date', ]
    ordering = ['title', 'group', 'teacher', 'date']
    list_filter = ['title', 'group', 'teacher', 'date']
    list_per_page = 10
    search_fields = ['title', 'group', 'teacher', 'date', 'notes']

    def view_on_site(self, obj):
        return reverse('exams-edit', kwargs={'pk': obj.id})


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Result)
admin.site.register(MonthJournal)