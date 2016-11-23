# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from django.template import loader

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from contact_form.forms import ContactForm

class MyContactForm(ContactForm):
    name = forms.CharField(
        max_length=100,
        label=u"Ваше ім'я"
    )

    email = forms.EmailField(
            label=u"Ваша Емейл Адреса"
        )

    user_subject = forms.CharField(
            label=u"Заголовок листа",
            max_length=128
        )
    body = forms.CharField(
            label=u"Текст повідомлення",
            max_length=2560,
            widget=forms.Textarea
        )
    field_order = ['name','email', 'user_subject', 'body']

    def __init__(self, request, *args, **kwargs):
        super(MyContactForm, self).__init__(request=request, *args, **kwargs)

        # use crispy forms
        self.helper = FormHelper()
        # form tag attributes
        self.helper.form_class = 'form-horisontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_form')
        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    # для відправки листа з html шаблоном
    def message(self):
        # html шаблон для відправки листів
        template_name = 'contact_form/html/contact_form.html'
        return loader.render_to_string(template_name,
                             self.get_context())

    def save(self, fail_silently=False):
        """
        Build and send the email message.

        """
        message_dict = self.get_message_dict()

        try:
            send_mail(fail_silently=fail_silently, html_message=message_dict['message'], **self.get_message_dict())
        except Exception, e:
            list(messages.get_messages(self.request))
            messages.warning(self.request, u"Під час відправки листа виникла непередбачувана " \
                                          u"помилка. Спробуйте скористатись даною формою пізніше.")
        else:
            list(messages.get_messages(self.request))
            messages.error(self.request, u'Повідомлення успішно надіслане!')

