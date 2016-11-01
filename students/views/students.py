# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from ..models.Student import Student
from ..models.Group import Group

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
    # Якщо форма була запощена: was form posted?
    if request.method == "POST":
        # Якщо кнопка Додати була натиснута: was form add button clicked?
        if request.POST.get('add_button') is not None:
            # errors collection
            errors ={}
            # data for student object
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            #validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday,'%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть корректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                student = Student(**data)
                # save it to database
                student.save()

                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(reverse('home'))

            # Якщо дані були введені некоректно:
            else:
                # Віддаємо шаблон форми разом із знайденими помилками
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})

        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            return HttpResponseRedirect(reverse('home'))

    # Якщо форма не була запощена:
    else:
        # Повертаємо код початкового стану форми
        return render(request,'students/students_add.html',
                  {'groups':Group.objects.all().order_by('title')})

def students_edit (request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete (request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

