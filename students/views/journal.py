# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

# Views for Journal
def journal(request):

    context = {}
    today = datetime.today()
    month = date(today.year, today.month, 1)

    next_month = month + relativedelta(months=1)
    prev_month = month - relativedelta(months=1)

    context['month_verbose'] = month.strftime('%B')
    context['year'] = month.year
    context['next_month'] = next_month.strftime('%Y-%m-%d')
    context['prev_month'] = prev_month.strftime('%Y-%m-%d')

    myear, mmonth = month.year, month.month
    number_of_days = monthrange(myear, mmonth)[1]
    context['month_header'] = [{'day': d,
                                'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
                               for d in range(1, number_of_days + 1)]

    days=[]
    for day in range(1, number_of_days+1):
        days.append({
            'day': day,
            'present': False,
        })

    t1 = [2, 3, 4, 5, 6, 8, ]
    t2 = [3, 4, 5, 6, 10, ]
    t3 = [4, 5, 9, ]
    import copy
    d1 = copy.deepcopy(days)
    d2 = copy.deepcopy(days)
    d3 = copy.deepcopy(days)
    for day in d1:
        if day['day'] in t1:
            day['present'] = True

    for day in d2:
        if day['day'] in t2:
            day['present'] = True

    for day in d3:
        if day['day'] in t3:
            day['present'] = True

    journal = [
        {
            'id': 1,
            'fullname': 'Подоба Віталій',
            'days': d1,
        },
        {
            'id': 2,
            'fullname': 'Корост Андрій',
            'days': d2,
        },
        {
            'id': 3,
            'fullname': 'Притула Тарас',
            'days': d3,
        },
    ]
    return render(request, 'students/journal.html', {'students': journal, 'context': context})
