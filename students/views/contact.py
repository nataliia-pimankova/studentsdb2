# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..forms import MyContactForm
from contact_form.views import ContactFormView


class MyContactFormView(ContactFormView):
    form_class = MyContactForm
    recipient_list = None
    template_name = 'contact_form/contact_form.html'

    def form_invalid(self, form):
        list(messages.get_messages(self.request))
        messages.warning(self.request, u'Виправте, будь-ласка, наступні помилки!')
        return self.render_to_response(self.get_context_data(form=form))


    def get_success_url(self):
        return reverse('contact_form_sent')
