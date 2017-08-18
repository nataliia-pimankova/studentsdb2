# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, \
    DeleteView, ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field

from django.contrib import messages

from ..models.students import Student
from ..util import paginate, get_current_group


# Views for Students.
class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template = 'students/student_list.html'

    def get_context_data(self, **kwargs):
        """This method adds extra variables to template"""
        # get original context data from parent class
        context = super(StudentList, self).get_context_data(**kwargs)

        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            students = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            students = Student.objects.all()

        # try to order students_list
        order_by = self.request.GET.get('order_by')
        if order_by in ('id', 'last_name', 'first_name', 'ticket'):
            students = students.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                students = students.reverse()
        else:
            students = students.order_by('last_name')

        # apply pagination, 10 students per page
        context['var_name'] = students
        context['students'] = students

        # apply pagination, 7 students per page
        # context = paginate(students, 7, self.request, {}, var_name='students')

        return context

    # def get_queryset(self):
    #     """Order students by last_name."""
    #     # get original query set
    #     qs = super(StudentList, self).get_queryset()
    #
    #     # order by last_name
    #     return qs.order_by('last_name')


def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # try to order students_list
    order_by = request.GET.get('order_by')
    if order_by in ('id','last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')

    # apply pagination, 7 students per page
    context = paginate(students, 7, request, {}, var_name='students')

    return render(request, 'students/students_list.html', context)


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ('last_name', 'first_name', 'middle_name', 'birthday',
                  'ticket', 'student_group', 'notes', 'photo')

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(StudentCreateForm, self).__init__(*args, **kwargs)

        # set form tag attributes
        self.form_action = reverse('students_add',
                     kwargs={})
        self.headline = u'Додати студента'

        self.form_method = 'POST'
        # self.form_class = 'form-horizontal'
        # self.novalidate = True

        self.helper = FormHelper(self)

        # set form field properties
        self.helper.form_tag = False
        # self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        # self.helper.label_class = 'col-sm-2 control-label'
        self.helper.label_class = 'col-lg-3'  # for example 'col-lg-2'
        self.helper.field_class = 'col-lg-9'  # for example 'col-lg-10'
        # self.helper.field_class = 'col-sm-9'
        layout = Layout(
            Field('last_name', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('first_name', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('middle_name', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('birthday', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('ticket', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('student_group', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('photo', css_class='form-control-static'),
            # Div('', css_class='col-sm-12 '),
            Field('notes', css_class='form-control-static')
        )
        self.helper.add_layout(layout)

        #form buttons
        self.helper.add_input(Submit('save_button', u'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-link'))
        self.helper.add_input(Reset('reset_button', u'Reset', css_class='btn btn-reset'))


class StudentUpdateForm(StudentCreateForm):

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.headline = u'Редагувати студента'


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'students/templates_add_edit.html'
    # form_class.title = u'Додати студента'

    def get_success_url(self):
        list(messages.get_messages(self.request))
        messages.success(self.request, u'Студент успішно доданий!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            list(messages.get_messages(self.request))
            messages.info(request,u'Додавання студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentCreateView, self).post(request,*args,**kwargs)

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'students/templates_add_edit.html'
    # form_class.title = u'Редагувати студента'

    def get_success_url(self):
        list(messages.get_messages(self.request))
        messages.success(self.request, u'Студента успішно збережено!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            list(messages.get_messages(self.request))
            messages.info(request,u'Редагування студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request,*args,**kwargs)



class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        list(messages.get_messages(self.request))
        messages.success(self.request,u'Студента успішно видалено!')
        return reverse('home')
