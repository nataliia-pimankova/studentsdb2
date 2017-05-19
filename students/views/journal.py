# -*- coding: utf-8 -*-
# from django.shortcuts import render
# from django.http import HttpResponse
# from datetime import datetime, date
# from dateutil.relativedelta import relativedelta
# from calendar import monthrange, weekday, day_abbr
#
# # Views for Journal
# def journal(request):
#
#     context = {}
#     today = datetime.today()
#     month = date(today.year, today.month, 1)
#
#     next_month = month + relativedelta(months=1)
#     prev_month = month - relativedelta(months=1)
#
#     context['month_verbose'] = month.strftime('%B')
#     context['year'] = month.year
#     context['next_month'] = next_month.strftime('%Y-%m-%d')
#     context['prev_month'] = prev_month.strftime('%Y-%m-%d')
#
#     myear, mmonth = month.year, month.month
#     number_of_days = monthrange(myear, mmonth)[1]
#     context['month_header'] = [{'day': d,
#                                 'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
#                                for d in range(1, number_of_days + 1)]
#
#     days=[]
#     for day in range(1, number_of_days+1):
#         days.append({
#             'day': day,
#             'present': False,
#         })
#
#     t1 = [2, 3, 4, 5, 6, 8, ]
#     t2 = [3, 4, 5, 6, 10, ]
#     t3 = [4, 5, 9, ]
#     import copy
#     d1 = copy.deepcopy(days)
#     d2 = copy.deepcopy(days)
#     d3 = copy.deepcopy(days)
#     for day in d1:
#         if day['day'] in t1:
#             day['present'] = True
#
#     for day in d2:
#         if day['day'] in t2:
#             day['present'] = True
#
#     for day in d3:
#         if day['day'] in t3:
#             day['present'] = True
#
#     journal = [
#         {
#             'id': 1,
#             'fullname': 'Подоба Віталій',
#             'days': d1,
#         },
#         {
#             'id': 2,
#             'fullname': 'Корост Андрій',
#             'days': d2,
#         },
#         {
#             'id': 3,
#             'fullname': 'Притула Тарас',
#             'days': d3,
#         },
#     ]
#     return render(request, 'students/journal.html', {'students': journal, 'context': context})
#
#
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models import MonthJournal, Student
from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')
        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{
            'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days + 1)]
            
        # витягуємо усіх студентів посортованих по
        queryset = Student.objects.order_by('last_name')
        # url to update student presence, for form post
        update_url = reverse('journal')
        # go over all students and collect data about presence
        # during selected month
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None
            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days + 1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day %d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            # prepare metadata for current student
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })
            
        # застосовуємо піганацію до списку студентів
        context = paginate(students, 10, self.request, context,
                           var_name='students')

        # finally return updated context
        # with paginated students
        return context
