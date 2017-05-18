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
from django.views.generic.base import TemplateView


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # перевіряємо чи передали нам місяць в параметрі,
        # якщо ні - вичисляємо поточний;
        # поки що ми віддаємо лише поточний:
        today = datetime.today()
        month = date(today.year, today.month, 1)

        # обчислюємо поточний рік, попередній і наступний місяці
        # а поки прибиваємо їх статично:
        context['prev_month'] = '2017-04-01'
        context['next_month'] = '2017-06-01'
        context['year'] = 2017

        # також поточний місяць;
        # змінну cur_month ми використовуватимемо пізніше
        # в пагінації; а month_verbose в
        # навігації помісячній:
        context['cur_month'] = '2017 - 05 - 01'
        context['month_verbose'] = u"Травень"
        # тут будемо обчислювати список днів у місяці,
        # а поки заб'ємо статично:
        context['month_header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Cр'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'}]
        # витягуємо усіх студентів посортованих по
        queryset = Student.objects.order_by('last_name')
        # це адреса для посту AJAX запиту, як бачите, ми
        # робитимемо його на цю ж в'юшку; в'юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу;
        update_url = reverse('journal')
        # пробігаємось по усіх студентах і збираємо
        # необхідні дані:
        students = []
        for student in queryset:
            # TODO: витягуємо журнал для студента і
            # вибраного місяця
            # набиваємо дні для студента
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2014, 7, day).strftime('%Y-%m-%d'),
                })
                # набиваємо усі решту даних студента
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })
        # застосовуємо піганацію до списку студентів
        context = paginate(students, 10, self.request, context,
                           var_name='students')
        # повертаємо оновлений словник із даними
        return context
