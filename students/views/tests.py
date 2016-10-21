# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse

from ..models.Test import Test

# Views for Students.

def tests_list (request):
    tests = Test.objects.all()

    # try to order tests_list
    order_by = request.GET.get('order_by')
    if order_by in ('title','teacher', 'group', 'date'):
        tests = tests.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            tests = tests.reverse()
    else :
        tests = tests.order_by('title')

    return render(request, 'students/tests_list.html',
                  {'tests': tests })

def tests_add (request):
    return HttpResponse('<h1>Test Add Form</h1>')

def tests_edit (request, tid):
    return HttpResponse('<h1>Edit Test %s</h1>' % tid)

def tests_delete (request, tid):
    return HttpResponse('<h1>Delete Test %s</h1>' % tid)

