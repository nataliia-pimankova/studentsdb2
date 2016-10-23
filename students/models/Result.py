# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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

    test = models.ForeignKey('Test',
        verbose_name=u"",
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    student = models.ForeignKey('Student',
        verbose_name=u"",
        blank=False,
        null=True,
        on_delete=models.CASCADE
    )


    def __unicode__(self):
        return u"%s - %s %s" % (self.grade, self.student, self.test)

