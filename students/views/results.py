from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field

from ..models import Student, Result, Group
from ..util import paginate, get_current_group


# Views for Results.
def results_list (request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)

    tid = request.GET.get('tid')
    sid = request.GET.get('sid')
    if tid:
        results = Result.objects.filter(exam=tid)
    elif sid:
        results = Result.objects.filter(student=sid)
    elif current_group:
        results = Result.objects.filter(exam__group=current_group)
    else:
        results = Result.objects.all()

    # apply pagination, 7 students per page
    context = paginate(results, 7, request, {}, var_name='results')

    return render(request, 'students/results_list.html', context)


class ResultCreateForm(ModelForm):

    class Meta:
        model = Result
        fields = ("exam", 'group', 'student', 'grade')

    def __init__(self, *args, **kwargs):

        # call original initializator
        super(ResultCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.form_action = reverse('results_add',
                     kwargs={})
        self.headline = _(u'Add Result')

        # self.helper.form_tag = True
        self.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.labels_uppercase = True

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        layout = Layout(
            Field('exam', css_class='form-control-static'),
            Field('group', css_class='form-control-static'),
            Field('student', css_class='form-control-static'),
            Field('grade', css_class='form-control-static'),
        )
        self.helper.add_layout(layout)

        # form buttons
        self.helper.add_input(Submit('save_button', _(u'Save'), css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class='btn btn-link'))


class ResultUpdateForm(ResultCreateForm):
    def __init__(self, *args, **kwargs):
        super(ResultUpdateForm, self).__init__(*args, **kwargs)
        self.form_action = reverse('results_edit',
                                   kwargs={'pk': kwargs['instance'].id})
        self.headline = _(u'Edit result')


class ResultCreateView(CreateView):
    model = Result
    form_class = ResultCreateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Result added successfully!'))
        return reverse('results')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, _(u'Result adding canceled!'))
            return HttpResponseRedirect(reverse('results'))
        else:
            return super(ResultCreateView, self).post(request,*args,**kwargs)


class ResultUpdateView(UpdateView):
    model = Result
    form_class = ResultUpdateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Result updated successfully!'))
        return reverse('results')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, _(u'Result updating canceled!'))
            return HttpResponseRedirect(reverse('results'))
        else:
            return super(ResultUpdateView, self).post(request,*args,**kwargs)


class ResultDeleteView(DeleteView):
    model = Result
    template_name = 'students/results_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Result deleted successfully!'))
        return reverse('results')

