# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Test(models.Model):
    """Test Model"""

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва предмету"
    )

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата і час проведення",
        null=True
    )

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач"
    )

    group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT
    )

    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки"
    )

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.title, self.group.title, self.teacher)

