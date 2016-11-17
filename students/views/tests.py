# coding=utf8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView

from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models.Test import Test

# Views for Students.

def tests_list (request):
    tests = Test.objects.all()

    # try to order tests_list
    order_by = request.GET.get('order_by')
    if order_by in ('title','teacher', 'group', 'date'):
        tests = tests.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            tests = tests.reverse()
    else :
        tests = tests.order_by('title')

    return render(request, 'students/tests_list.html',
                  {'tests': tests })

class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(TestForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if hasattr(kwargs['instance'], 'id'):
            self.helper.form_action = reverse('tests_edit',
                                              kwargs={'pk': kwargs['instance'].id})
            self.headline = u'Редагувати іспит'
        else:
        # set form tag attributes
            self.helper.form_action = reverse('tests_add',
                         kwargs={})
            self.headline = u'Додати іспит'

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

class TestCreateView(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'students/groups_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Іспит успішно доданий!')
        return reverse('tests')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, u'Додавання іспиту скасовано!')
            return HttpResponseRedirect(reverse('tests'))
        else:
            return super(TestCreateView, self).post(request,*args,**kwargs)


class TestUpdateView(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'students/groups_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Іспит успішно збережено!')
        return  reverse('tests')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, u'Редагування іспиту відмінено!')
            return HttpResponseRedirect(reverse('tests'))
        else:
            return super(TestUpdateView, self).post(request,*args,**kwargs)


class TestDeleteView(DeleteView):
    model = Test
    template_name = 'students/tests_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Іспит успішно видалено!')
        return reverse('tests')

