# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse

from ..models.Student import Student

# Views for Students.

def students_list (request):
    students = Student.objects.all()

    # try to order students_list
    order_by = request.GET.get('order_by')
    if order_by in ('id','last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else :
        students = students.order_by('last_name')

    page = request.GET.get('page')

    try:
        page = int(page)
    except(ValueError, TypeError):
        # if 'home'
        page = 1

    per_page = 3
    num_pages, remainder = divmod(Student.objects.count() , per_page)
    if remainder :
        num_pages +=1

    if  page < 1:
        page = 1
    elif page > num_pages:
        page = num_pages

    start = (int(page)-1)*per_page
    limit = start + per_page
    students = students[start: limit]

    if num_pages > 1:
        students.has_other_pages = True
    else:
        students.has_other_pages = False

    students.page_range = range(1, num_pages+1)
    students.page = page

    return render(request, 'students/students_list.html',
                  {'students': students })

def students_add (request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit (request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete (request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

