from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from ..forms import MyContactForm
from contact_form.views import ContactFormView


class MyContactFormView(ContactFormView):
    form_class = MyContactForm
    recipient_list = None
    template_name = 'contact_form/contact_form.html'

    def form_invalid(self, form):
        list(messages.get_messages(self.request))
        messages.warning(self.request, _(u'Please, correct the following errors.'))
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('contact_form_sent')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyContactFormView, self).dispatch(*args, **kwargs)
