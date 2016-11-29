"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from students.views import students, groups, journal, tests, results, contact_admin
from .settings import MEDIA_ROOT, DEBUG
from django.views import static
from students.views.students import StudentCreateView, StudentUpdateView, StudentDeleteView
from students.views.groups import GroupCreateView, GroupUpdateView, GroupDeleteView
from students.views.tests import TestCreateView, TestUpdateView, TestDeleteView
from students.views.results import ResultCreateView, ResultUpdateView, ResultDeleteView
from students.views.contact_admin import ContactView

from django.views.generic import TemplateView
from students.forms import MyContactForm
from students.views.contact import MyContactFormView

urlpatterns = [
    # Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$', StudentCreateView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),

    # Journal Urls
    url(r'^journal/$', journal.journal, name='journal'),

    # Tests Urls
    url(r'^tests/$', tests.tests_list, name='tests'),
    url(r'^tests/add/$', TestCreateView.as_view(), name='tests_add'),
    url(r'^tests/(?P<pk>\d+)/edit/$', TestUpdateView.as_view(), name='tests_edit'),
    url(r'^tests/(?P<pk>\d+)/delete/$', TestDeleteView.as_view(), name='tests_delete'),

    # Results Urls
    url(r'^results/$', results.results_list, name='results'),
    url(r'^results/add/$', ResultCreateView.as_view(), name='results_add'),
    url(r'^results/(?P<pk>\d+)/edit/$', ResultUpdateView.as_view(), name='results_edit'),
    url(r'^results/(?P<pk>\d+)/delete/$', ResultDeleteView.as_view(), name='results_delete'),

    # Contact Admin Form
    url(r'^contact_admin/$', ContactView.as_view(), name='contact_admin'),
    url(r'^contact/$', MyContactFormView.as_view(form_class=MyContactForm),name='contact_form'),
    url(r'^contact/sent/$', TemplateView.as_view(template_name='contact_form/contact_form_sent.html'), name='contact_form_sent'),

    url(r'^admin/', include(admin.site.urls)),
]

if DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', static.serve,
                       {'document_root': MEDIA_ROOT}),
                    ]