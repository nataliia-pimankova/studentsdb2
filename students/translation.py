from modeltranslation.translator import translator, TranslationOptions
from students.models import Student, Group, Exam


class StudentTranslationOptions(TranslationOptions):
    """
    class settings for the internationalization of model fields Student.
    """

    fields = ('first_name', 'last_name', 'middle_name')


class GroupTranslationOptions(TranslationOptions):
    """
    class settings for the internationalization of model fields Group.
    """

    fields = ('title', )


class ExamTranslationOptions(TranslationOptions):
    """
    class settings for the internationalization of model fields Group.
    """

    fields = ('title', 'teacher', )


translator.register(Exam, ExamTranslationOptions)
translator.register(Student, StudentTranslationOptions)
translator.register(Group, GroupTranslationOptions)
