# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse


# Views for Groups
def groups_list (request):
    groups = (
        {   'id': 1,
            'name': u'МтМ-21',
            'captain': u'Ячменев Олег',
        },
        {   'id': 2,
            'name': u'МтМ-22',
            'captain': u'Подоба Віталій',
        },
        {   'id': 3,
            'name': u'МтМ-23',
            'captain': u'Іванов Андрій',
        },
    )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add (request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit (request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete (request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

