from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'grade')

# Register your models here
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)