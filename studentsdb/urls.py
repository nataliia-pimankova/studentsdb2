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
from students.views import students, groups, journal, tests
from .settings import MEDIA_ROOT, DEBUG
from django.views import static

urlpatterns = [
    # Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$', students.students_edit, name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$', students.students_delete, name='students_delete'),

    # Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),

    # Journal Urls
    url(r'^journal/$', journal.journal, name='journal'),

    # Tests Urls
    url(r'^tests/$', tests.tests_list, name='tests'),
    url(r'^tests/add/$', tests.tests_add, name='tests_add'),
    url(r'^tests/(?P<tid>\d+)/edit/$', tests.tests_edit, name='tests_edit'),
    url(r'^tests/(?P<tid>\d+)/delete/$', tests.tests_delete, name='tests_delete'),

    url(r'^admin/', include(admin.site.urls)),
]

if DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', static.serve,
                       {'document_root': MEDIA_ROOT}),
                    ]