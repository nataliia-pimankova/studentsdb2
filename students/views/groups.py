# coding=utf8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages

from ..models.Group import Group
from ..util import paginate


# Views for Groups
class GroupList(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'students/groups_list.html'

    def get_context_data(self, **kwargs):
        """This method adds extra variables to template"""
        # get original context data from parent class
        context = super(GroupList, self).get_context_data(**kwargs)

        groups = Group.objects.all()

        # try to order groups_list
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('id', 'title', 'leader'):
            groups = groups.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                groups = groups.reverse()

        # apply pagination, 10 students per page
        context = paginate(groups, 5, self.request, context, var_name='groups')

        # return context mapping
        return context


class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'leader','notes')

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.form_action = reverse('groups_add',
                     kwargs={})
        self.headline = u'Додати групу'

        # self.helper.form_tag = True
        self.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.labels_uppercase = True

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        #form buttons
        self.helper.add_input(Submit('save_button', u'Зберегти', css_class='btn btn-primary'))
        self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class='btn btn-link'))

class GroupUpdateForm(GroupCreateForm):
    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.form_action = reverse('groups_edit',
                                   kwargs={'pk': kwargs['instance'].id})
        self.headline = u'Редагувати групу'

class GroupCreateView(CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Група успішно додана!')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, u'Додавання групи скасовано!')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupCreateView, self).post(request,*args,**kwargs)


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupUpdateForm
    template_name = 'students/templates_add_edit.html'

    def get_success_url(self):
        messages.success(self.request, u'Групу успішно збережено!')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.info(request, u'Редагування групи відмінено!')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request,*args,**kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u'Групу успішно видалено!')
        return reverse('groups')

