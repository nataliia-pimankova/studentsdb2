# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse

from ..models.Result import Result

# Views for Results.
def results_list (request):
    tid = request.GET.get('tid')
    sid = request.GET.get('sid')
    if tid:
        results = Result.objects.filter(test=tid)
    elif sid:
        results = Result.objects.filter(student=sid)
    else:
        results = Result.objects.all()

    return render(request, 'students/results_list.html',
                  {'results': results })


def results_add (request):
    return HttpResponse('<h1>Result Add Form</h1>')

def results_edit (request, rid):
    return HttpResponse('<h1>Edit Result %s</h1>' % rid)

def results_delete (request, rid):
    return HttpResponse('<h1>Delete Result %s</h1>' % rid)

