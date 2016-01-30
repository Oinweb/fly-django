from modeltranslation.translator import register, TranslationOptions
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from api.models import Badge
from api.models import Course
from api.models import Quiz
from api.models import Question


@register(Badge)
class BadgeTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'description',)


@register(Quiz)
class QuizTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'a', 'b', 'c', 'd', 'e', 'f', 'true_choice', 'false_choice',)




class BadgeAdmin(TranslationAdmin):
    pass
admin.site.register(Badge, BadgeAdmin)

class CourseAdmin(TranslationAdmin):
    pass
admin.site.register(Course, CourseAdmin)

class QuizAdmin(TranslationAdmin):
    pass
admin.site.register(Quiz, QuizAdmin)

class QuestionAdmin(TranslationAdmin):
    pass
admin.site.register(Question, QuestionAdmin)