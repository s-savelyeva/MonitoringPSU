from django.contrib import admin
from .models import Student, Staff, Guest, Test, Question, Choice, UserTest, UserAnswer, Scale, Result
from .models import Faculty, TelegramProfile, BachSpecDirection, MasterDirection, PhdDirection, BachSpecProfile, MasterProfile, PhdProfile

class ProfileStudent(admin.ModelAdmin):
    list_display = ['user', 'patronymic', 'date_of_birth', 'role', 'faculty', 'grade', 'direction', 'profile', 'study_form', 'education_level']

class ProfileStaff(admin.ModelAdmin):
    list_display = ['user', 'patronymic', 'date_of_birth', 'role', 'faculty']
    
class ProfileGuest(admin.ModelAdmin):
    list_display = ['user', 'patronymic', 'date_of_birth', 'role']

class ProfileTest(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_at', 'updated_at']

class ProfileQuestion(admin.ModelAdmin):
    list_display = ['test', 'question_text', 'question_type', 'is_mandatory']

class ProfileChoice(admin.ModelAdmin):
    list_display = ['question', 'choice_text', 'score']

class ProfileUserTest(admin.ModelAdmin):
    list_display = ['user', 'test', 'result', 'completed_at', 'result_description', 'additional_info', 'completed_at']

class ProfileUserAnswer(admin.ModelAdmin):
    list_display = ['user_test', 'question', 'chosen_choice', 'score']

class ProfileScale(admin.ModelAdmin):
    list_display = ['question', 'min_sign', 'max_sign', 'min_score', 'max_score', 'type', 'inverse']

class ProfileResult(admin.ModelAdmin):
    list_display = ['test', 'min_score', 'max_score', 'result_description', 'additional_info']

class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class BachSpecDirectionAdmin(admin.ModelAdmin):
    list_display = ['direction_name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['direction_name', 'faculty__name']

class MasterDirectionAdmin(admin.ModelAdmin):
    list_display = ['direction_name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['direction_name', 'faculty__name']

class PhdDirectionAdmin(admin.ModelAdmin):
    list_display = ['direction_name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['direction_name', 'faculty__name']

class BachSpecProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'direction', 'level', 'education_form', 'number_of_courses']
    list_filter = ['direction', 'education_form']
    search_fields = ['profile', 'direction__direction_name', 'direction__faculty__name']

class MasterProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'direction', 'education_form', 'number_of_courses']
    list_filter = ['direction', 'education_form']
    search_fields = ['profile', 'direction__direction_name', 'direction__faculty__name']

class PhdProfileAdmin(admin.ModelAdmin):
    list_display = ['profile', 'direction', 'education_form', 'number_of_courses']
    list_filter = ['direction', 'education_form']
    search_fields = ['profile', 'direction__direction_name', 'direction__faculty__name']

class TelegramProfileAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'telegram_username']


admin.site.register(Student, ProfileStudent)
admin.site.register(Staff, ProfileStaff)
admin.site.register(Guest, ProfileGuest)
admin.site.register(Test, ProfileTest)
admin.site.register(Question, ProfileQuestion)
admin.site.register(Choice, ProfileChoice)
admin.site.register(UserTest, ProfileUserTest)
admin.site.register(UserAnswer, ProfileUserAnswer)
admin.site.register(Scale, ProfileScale)
admin.site.register(Result, ProfileResult)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(BachSpecDirection, BachSpecDirectionAdmin)
admin.site.register(MasterDirection, MasterDirectionAdmin)
admin.site.register(PhdDirection, PhdDirectionAdmin)
admin.site.register(BachSpecProfile, BachSpecProfileAdmin)
admin.site.register(MasterProfile, MasterProfileAdmin)
admin.site.register(PhdProfile, PhdProfileAdmin)
admin.site.register(TelegramProfile, TelegramProfileAdmin)


