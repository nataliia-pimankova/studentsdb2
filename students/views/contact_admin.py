import logging

from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):
    def __init__(self, *args, **kwards):
        # call original initializator
        super(ContactForm, self).__init__(*args, **kwards)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        # self.helper.form_class = 'form-horizontal'
        self.form_method = 'post'
        self.helper.form_tag = False
        self.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', _(u'Send')))

    from_email = forms.EmailField(
        label=_(u"Your Email Address")
    )

    subject = forms.CharField(
        label=_(u"Email Subject"),
        max_length=128
    )
    message = forms.CharField(
        label=_(u"Email Body"),
        max_length=2560,
        widget=forms.Textarea
    )


def contact_admin(request):
    # check it form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                message = _(u"An error occured during email transfer. Please, "
                            u"try again later.")
                messages.warning(request, message)
                logger = logging.getLogger(__name__)
                logger.exception(message)
            else:
                message = _(u'Message sent successfully!')
                messages.success(request, message)

            # redirect to same contact page with success message
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there was not POST render blank form
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})


class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    # success_url = '/email-sent/'
    success_url = '/contact_admin/'

    def get_success_url(self):
        return reverse('contact_admin')

    def form_valid(self, form):
        """This method is called for valid data"""
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        try:
            send_mail(subject, message, from_email, [ADMIN_EMAIL])
        except Exception:
            message = _(u"An error occured during email transfer. Please, "
                            u"try again later.")
            messages.warning(self.request, message)
            logger = logging.getLogger(__name__)
            logger.exception(message)
        else:
            message = _(u'Message sent successfully!')
            messages.success(self.request, message)

        return super(ContactView, self).form_valid(form)
