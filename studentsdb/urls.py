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
from students.views import students, groups, exams, results, contact_admin
from .settings import MEDIA_ROOT, DEBUG
from django.views import static
from students.views.contact_admin import ContactView
from students.views.journal import JournalView
from django.views.i18n import JavaScriptCatalog
from django.views.generic import TemplateView
from students.forms import MyContactForm
from students.views.contact import MyContactFormView


urlpatterns = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    # Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^student_list/$', students.StudentList.as_view(), name='student_list'),
    url(r'^students/add/$', students.StudentCreateView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', students.StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', students.StudentDeleteView.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', groups.GroupList.as_view(), name='groups'),
    url(r'^groups/add/$', groups.GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', groups.GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', groups.GroupDeleteView.as_view(), name='groups_delete'),

    # Journal Urls
    # url(r'^journal/$', journal.journal, name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Tests Urls
    url(r'^exams/$', exams.ExamList.as_view(), name='exams'),
    url(r'^exams/add/$', exams.ExamCreateView.as_view(), name='exams-add'),
    url(r'^exams/(?P<pk>\d+)/edit/$', exams.ExamUpdateView.as_view(), name='exams-edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$', exams.ExamDeleteView.as_view(), name='exams-delete'),

    # Results Urls
    url(r'^results/$', results.results_list, name='results'),
    url(r'^results/add/$', results.ResultCreateView.as_view(), name='results_add'),
    url(r'^results/(?P<pk>\d+)/edit/$', results.ResultUpdateView.as_view(), name='results_edit'),
    url(r'^results/(?P<pk>\d+)/delete/$', results.ResultDeleteView.as_view(), name='results_delete'),

    # Contact Admin Form
    url(r'^contact_admin/$', ContactView.as_view(), name='contact_admin'),
    url(r'^contact/$', MyContactFormView.as_view(form_class=MyContactForm),name='contact_form'),
    url(r'^contact/sent/$', TemplateView.as_view(template_name='contact_form/contact_form_sent.html'), name='contact_form_sent'),

    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

if DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', static.serve,
                       {'document_root': MEDIA_ROOT}),
                    ]