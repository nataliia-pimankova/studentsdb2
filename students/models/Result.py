from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class Result(models.Model):
    """Result Model"""

    class Meta(object):
        verbose_name = _(u"Result")
        verbose_name_plural = _(u"Results")

    grade = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_(u"Grade")
    )

    exam = models.ForeignKey(
        'Exam',
        verbose_name=_(u"Exam"),
        blank=False,
        null=True,
        on_delete=models.SET_NULL
    )

    group = ChainedForeignKey(
        'Group',
        chained_field='exam',
        chained_model_field='exam',
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
        return u"%s - %s %s" % (self.grade, self.student, self.exam)

