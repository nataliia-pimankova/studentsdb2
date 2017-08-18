# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class Result(models.Model):
    """Result Model"""

    class Meta(object):
        verbose_name = u"Результат"
        verbose_name_plural = u"Результати"

    grade = models.FloatField(
        blank=True,
        null=True,
        verbose_name=u"Оцінка"
    )

    test = models.ForeignKey(
        'Test',
        verbose_name=u"Іспит",
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    group = ChainedForeignKey(
        'Group',
        chained_field='test',
        chained_model_field='test',
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True
    )

    student = ChainedForeignKey(
        'Student',
        chained_field="group",
        chained_model_field="student_group",
        show_all=False,
        auto_choose=True,
        sort=True)

    def __unicode__(self):
        return u"%s - %s %s" % (self.grade, self.student, self.test)

