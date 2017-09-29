from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models.Exam import Exam
from ..util import paginate, get_current_group


# Views for Tests.
class ExamList(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'students/exams_list.html'

    def get_context_data(self, **kwargs):
        """This method adds extra variables to template"""
        # get original context data from parent class
        context = super(ExamList, self).get_context_data(**kwargs)

        # tell template not to show logo on a page
        context['show_logo'] = False

        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            tests = Exam.objects.filter(group=current_group)
        else:
            # otherwise show all students
            tests = Exam.objects.all()

        # try to order tests_list
        order_by = self.request.GET.get('order_by')
        if order_by in ('id', 'title', 'teacher', 'group', 'date'):
            tests = tests.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                tests = tests.reverse()
        else:
            tests = tests.order_by('title')

        # apply pagination, 10 students per page
        context = paginate(tests, 7, self.request, context, var_name='exams')

        # return context mapping
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamList, self).dispatch(*args, **kwargs)


class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'date', 'teacher', 'group', 'notes']

    def __init__(self, instance, *args, **kwargs):
        # call original initializator
        super(ExamCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exams-add',
                                          kwargs={})
        self.headline = _(u'Add Exam')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('save_button', _(u'Save'), css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class='btn btn-link'))


class ExamUpdateForm(ExamCreateForm):
    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)
        self.form_action = reverse('exams-edit',
                                   kwargs={'pk': kwargs['instance'].id})
        print(kwargs['instance'].id)
        self.headline = _(u'Edit exam')


class ExamCreateView(CreateView):
    model = Exam
    form_class = ExamCreateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Exam added successfully!!'))
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, _(u'Exam adding canceled!'))
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamCreateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamCreateView, self).dispatch(*args, **kwargs)


class ExamUpdateView(UpdateView):
    model = Exam
    form_class = ExamUpdateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Exam updated successfully!'))
        return reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, _(u'Exam updating canceled!'))
            return HttpResponseRedirect(reverse('exams'))
        else:
            return super(ExamUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamUpdateView, self).dispatch(*args, **kwargs)


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exam_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Exam deleted successfully!'))
        return reverse('exams')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExamDeleteView, self).dispatch(*args, **kwargs)
