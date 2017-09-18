from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = _(u"Exam")
        verbose_name_plural = _(u"Exams")

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Title of Subject")
    )

    date = models.DateTimeField(
        blank=False,
        verbose_name=_(u"Date and Time"),
        null=True
    )

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Teacher")
    )

    group = models.ForeignKey('Group',
        verbose_name=_(u"Group"),
        blank=False,
        null=True,
        on_delete=models.PROTECT
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Notes")
    )

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.title, self.group.title, self.teacher)

