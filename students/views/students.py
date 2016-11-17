# coding=utf8
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages

from ..models.Student import Student
from ..models.Group import Group



# Views for Students.

def students_list (request):
    students = Student.objects.all()

    # try to order students_list
    order_by = request.GET.get('order_by')
    if order_by in ('id','last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else :
        students = students.order_by('last_name')

    page = request.GET.get('page')

    try:
        page = int(page)
    except(ValueError, TypeError):
        # if 'home'
        page = 1

    per_page = 7
    num_pages, remainder = divmod(Student.objects.count() , per_page)
    if remainder :
        num_pages +=1

    if  page < 1:
        page = 1
    elif page > num_pages:
        page = num_pages

    start = (int(page)-1)*per_page
    limit = start + per_page
    students = students[start: limit]

    if num_pages > 1:
        students.has_other_pages = True
    else:
        students.has_other_pages = False

    students.page_range = range(1, num_pages+1)
    students.page = page

    return render(request, 'students/students_list.html',
                  {'students': students })

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(StudentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if hasattr(kwargs['instance'], 'id'):
            self.helper.form_action = reverse('students_edit',
                                              kwargs={'pk': kwargs['instance'].id})
            self.headline = u'Редагувати студента'
        else:
        # set form tag attributes
            self.helper.form_action = reverse('students_add',
                         kwargs={})
            self.headline = u'Додати студента'

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        #form buttons
        self.helper.add_input(Submit('save_button', u'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-link'))

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/students_edit.html'
    # form_class.title = u'Додати студента'

    def get_success_url(self):
        messages.success(self.request, u'Студент успішно доданий!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request,u'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentCreateView, self).post(request,*args,**kwargs)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/students_edit.html'
    # form_class.title = u'Редагувати студента'

    def get_success_url(self):
        messages.success(self.request, u'Студента успішно збережено!')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request,u'Редагування студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request,*args,**kwargs)



class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request,u'Студента успішно видалено!')
        return reverse('home')
