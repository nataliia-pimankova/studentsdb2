# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from students.models import Student


class StudentTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Page.
    """

    fields = ('first_name', 'last_name', 'middle_name', 'notes')

translator.register(Student, StudentTranslationOptions)
