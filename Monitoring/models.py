# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_profile')
    telegram_id = models.BigIntegerField(unique=True, verbose_name="ID в Telegram")
    telegram_username = models.CharField(max_length=150, blank=True, verbose_name="Имя пользователя в Telegram")

    class Meta:
        verbose_name = "Профиль Telegram"
        verbose_name_plural = "Профили Telegram"

    def __str__(self):
        return f"{self.user.username}: {self.telegram_username}"

#Модель для студента
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    patronymic = models.CharField('Отчество', max_length=100, blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    role = models.CharField('Роль', max_length=50, default='Студент')
    faculty = models.CharField('Факультет', max_length=200, blank=True, null=True)
    education_level = models.CharField('Уровень образования', max_length=50, blank=True, null=True)
    direction = models.CharField('Направление', max_length=200, blank=True, null=True)
    profile = models.CharField('Профиль', max_length=200, blank=True, null=True)
    study_form = models.CharField('Форма обучения', max_length=200, blank=True, null=True)
    grade = models.CharField('Курс', max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Студент: {self.user.get_full_name()}"
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

#Модель для сотрудника
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    date_of_birth = models.DateField(blank=True, null=True)
    patronymic = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)

    def __str__(self):
        return f"Сотрудник: {self.user.username}"
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

#Модель для гостя
class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest')
    date_of_birth = models.DateField(blank=True, null=True)
    patronymic = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, default="Гость", blank=True, null=True)
    
    def __str__(self):
        return f"Гость: {self.user.username}"
    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'
    
#Модель для теста
class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    assigned_categories = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.title
    def is_available_for_user(self, user):
        if self.assigned_categories == 'all':
            return True
        if hasattr(user, 'student') and 'student' in self.assigned_categories:
            return True
        if hasattr(user, 'staff') and 'staff' in self.assigned_categories:
            return True
        if hasattr(user, 'guest') and 'guest' in self.assigned_categories:
            return True
        return False
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
    
#Модель для вопросов
class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, blank=True, null=True)
    is_mandatory = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
    
#Варианты ответов на вопросы тестов с баллами
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.choice_text
    class Meta:
        verbose_name = 'Ответ - один из списка'
        verbose_name_plural = 'Ответы - один из списка'
    
class Scale(models.Model):
    SCALE_TYPE_CHOICES = [
        ('default', 'Стандартная'),
        ('twoside', 'Двусторонняя'),
        ('minus', 'Отрицательная'),
    ]
    question = models.ForeignKey(Question, related_name='scales', on_delete=models.CASCADE)
    min_sign = models.CharField(max_length=200)
    max_sign = models.CharField(max_length=200)
    min_score = models.IntegerField(null=False, blank=False, default=0)
    max_score = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=200, choices=SCALE_TYPE_CHOICES, default="default")
    inverse = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.min_sign} - {self.max_sign}'
    class Meta:
        verbose_name = 'Ответ - шкала'
        verbose_name_plural = 'Ответы - шкала'

# Модель назначения пользователю теста
class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    result_description = models.CharField(max_length=500, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.test.title}'
    class Meta:
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'


#Модель для хранения ответов пользователей
class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'Answer by {self.user_test.user.username} for {self.question}'
    class Meta:
        verbose_name = 'Балл за вопрос'
        verbose_name_plural = 'Баллы за вопросы'

class Result(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    min_score = models.IntegerField()
    max_score = models.IntegerField(null=True, blank=True)
    result_description = models.CharField(max_length=500, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    condition = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='result_images/', null=True, blank=True)
    COLOR_DIRECTION_CHOICES = [
        ('green_to_red', 'От зеленого к красному'),
        ('red_to_green', 'От красного к зеленому'),
    ]
    use_thermometer = models.BooleanField(default=False)
    color_direction = models.CharField(
        max_length=20, 
        choices=COLOR_DIRECTION_CHOICES, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'{self.test.title} - {self.min_score} to {self.max_score} with condition {self.condition}'
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Все возможные результаты'

class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Факультет')
    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
    def __str__(self):
        return self.name


class BachSpecDirection(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='bachspec_directions', verbose_name='Факультет')
    direction_name = models.CharField(max_length=200, verbose_name='Направление')

    class Meta:
        unique_together = ('faculty', 'direction_name')
        verbose_name = 'Направление (Бакалавриат/Специалитет)'
        verbose_name_plural = 'Направления (Бакалавриат/Специалитет)'

    def __str__(self):
        return f"{self.direction_name} [Бакалавриат/Специалитет, {self.faculty.name}]"


class MasterDirection(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='master_directions', verbose_name='Факультет')
    direction_name = models.CharField(max_length=200, verbose_name='Направление')

    class Meta:
        unique_together = ('faculty', 'direction_name')
        verbose_name = 'Направление (Магистратура)'
        verbose_name_plural = 'Направления (Магистратура)'

    def __str__(self):
        return f"{self.direction_name} [Магистратура, {self.faculty.name}]"


class PhdDirection(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='phd_directions', verbose_name='Факультет')
    direction_name = models.CharField(max_length=200, verbose_name='Направление')

    class Meta:
        unique_together = ('faculty', 'direction_name')
        verbose_name = 'Направление (Аспирантура)'
        verbose_name_plural = 'Направления (Аспирантура)'

    def __str__(self):
        return f"{self.direction_name} [Аспирантура, {self.faculty.name}]"


class BachSpecProfile(models.Model):
    LEVEL_CHOICES = [
        ('бакалавриат', 'Бакалавриат'),
        ('специалитет', 'Специалитет')
    ]
    EDUCATION_FORMS = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('очно-заочная', 'Очно-заочная'),
    ]
    direction = models.ForeignKey(BachSpecDirection, on_delete=models.CASCADE, related_name='profiles', verbose_name='Направление', null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Уровень (бакалавриат/специалитет)' , null=True, blank=True )
    profile = models.CharField(max_length=200, verbose_name='Профиль')
    education_form = models.CharField(max_length=20, choices=EDUCATION_FORMS, verbose_name='Форма обучения')
    number_of_courses = models.PositiveIntegerField(verbose_name='Количество курсов')

    class Meta:
        verbose_name = 'Профиль (Бакалавриат/Специалитет)'
        verbose_name_plural = 'Профили (Бакалавриат/Специалитет)'

    def __str__(self):
        return f"{self.profile} ({self.get_level_display()}) [{self.direction}]"


class MasterProfile(models.Model):
    EDUCATION_FORMS = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('очно-заочная', 'Очно-заочная'),
    ]
    direction = models.ForeignKey(MasterDirection, on_delete=models.CASCADE, related_name='profiles', verbose_name='Направление', null=True, blank=True )
    profile = models.CharField(max_length=200, verbose_name='Профиль')
    education_form = models.CharField(max_length=20, choices=EDUCATION_FORMS, verbose_name='Форма обучения')
    number_of_courses = models.PositiveIntegerField(verbose_name='Количество курсов')

    class Meta:
        verbose_name = 'Профиль (Магистратура)'
        verbose_name_plural = 'Профили (Магистратура)'

    def __str__(self):
        return f"{self.profile} [{self.direction}]"


class PhdProfile(models.Model):
    EDUCATION_FORMS = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('очно-заочная', 'Очно-заочная'),
    ]
    direction = models.ForeignKey(PhdDirection, on_delete=models.CASCADE, related_name='profiles', verbose_name='Направление', null=True, blank=True )
    profile = models.CharField(max_length=200, verbose_name='Профиль')
    education_form = models.CharField(max_length=20, choices=EDUCATION_FORMS, verbose_name='Форма обучения')
    number_of_courses = models.PositiveIntegerField(verbose_name='Количество курсов')

    class Meta:
        verbose_name = 'Профиль (Аспирантура)'
        verbose_name_plural = 'Профили (Аспирантура)'

    def __str__(self):
        return f"{self.profile} [{self.direction}]"

