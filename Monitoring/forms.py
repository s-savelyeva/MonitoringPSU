from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import Student, Staff, BachSpecDirection, PhdDirection, MasterDirection, PhdProfile, MasterProfile,  BachSpecProfile, Guest, Test, Question, Faculty, Scale, Choice  #Импорт наших моделей студентов и сотрудников

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Регистрация
class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин',
            'maxlength': '15',
            'class': 'number-phone-registration',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'maxlength': '50',
            'class': 'password-registration',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль повторно',
            'maxlength': '50',
            'class': 'password-registration-repeat',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    class Meta:
        model = User
        fields = ['phone_number', 'password', 'password_repeat']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password != password_repeat:
            raise forms.ValidationError("Пароли не совпадают")
    

# Персональные данные
class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите вашу фамилию',
            'class': 'surname',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя',
            'class': 'name',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


# 
class CommonProfileForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        widget=forms.Select(attrs={
            'class': 'text-message-for-comformation',
        }),
        empty_label="Выберите факультет",
        label='Факультет'
    )
    class Meta:
        fields = ('faculty',)


class StudentEditForm(CommonProfileForm):
    EDUCATION_LEVEL_CHOICES = [
        ('бакалавриат', 'Бакалавриат'),
        ('специалитет', 'Специалитет'),
        ('магистратура', 'Магистратура'),
        ('аспирантура', 'Аспирантура'),
    ]
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше отчество',
            'class': 'text-message-for-comformation',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'Выберите дату рождения',
            'class': 'text-message-for-comformation',
            'type': 'date',
        }),
        label='Дата рождения',
        input_formats=['%Y-%m-%d'],
    )
    role = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'placeholder': 'Введите вашу роль',
            'class': 'text-message-for-comformation',
            'autocomplete': 'new-password',
        }),
        label='Роль'
    )
    education_level = forms.ChoiceField(
        choices=EDUCATION_LEVEL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'text-message-for-comformation',
            'id': 'id_education_level'
        }),
        label='Уровень образования'
    )
    direction = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'text-message-for-comformation',
            'id': 'id_direction'
        }),
        label='Направление'
    )
    profile = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'text-message-for-comformation',
            'id': 'id_profile'
        }),
        label='Профиль'
    )
    education_form = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'text-message-for-comformation',
            'id': 'id_education_form',
        }),
        label='Форма обучения'
    )
    grade = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'text-message-for-comformation',
            'autocomplete': 'new-password',
        }),
        label='Курс'
    )
    class Meta(CommonProfileForm.Meta):
        model = Student
        fields = CommonProfileForm.Meta.fields + (
            'patronymic', 'date_of_birth', 'role',
            'education_level', 'direction', 'profile',
            'education_form', 'grade'
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].choices = [('', 'Выберите факультет')] + [
            (str(f.id), f.name) for f in Faculty.objects.all()
        ]
        data = kwargs.get('data') or (args[0] if args else None)
        education_level = ''
        faculty_id = ''
        direction_id = ''
        profile_id = ''
        def choose_valid_id(value):
            if isinstance(value, list):
                for v in value:
                    v = str(v).strip()
                    if v:
                        return v
                return ''
            elif value:
                return str(value).strip()
            return ''
        if data:
            education_level = data.get('education_level', '')
            faculty_id = choose_valid_id(data.get('faculty', ''))
            direction_id = choose_valid_id(data.get('direction', ''))
            profile_id = choose_valid_id(data.get('profile', ''))
        elif self.instance:
            education_level = self.instance.education_level or ''
            faculty_id = self.instance.faculty or ''
            direction_id = self.instance.direction or ''
            profile_id = self.instance.profile or ''

        if education_level and faculty_id:
            if education_level in ['бакалавриат', 'специалитет']:
                qs = BachSpecDirection.objects.filter(faculty_id=faculty_id)
            elif education_level == 'магистратура':
                qs = MasterDirection.objects.filter(faculty_id=faculty_id)
            elif education_level == 'аспирантура':
                qs = PhdDirection.objects.filter(faculty_id=faculty_id)
            else:
                qs = []
            self.fields['direction'].choices = [('', 'Выберите направление')] + [(str(d.id), d.direction_name) for d in qs]
        else:
            self.fields['direction'].choices = [('', 'Выберите направление')]

        if direction_id and education_level:
            if education_level in ['бакалавриат', 'специалитет']:
                qs = BachSpecProfile.objects.filter(direction_id=direction_id)
            elif education_level == 'магистратура':
                qs = MasterProfile.objects.filter(direction_id=direction_id)
            elif education_level == 'аспирантура':
                qs = PhdProfile.objects.filter(direction_id=direction_id)
            else:
                qs = []
            self.fields['profile'].choices = [('', 'Выберите профиль')] + [(str(p.id), p.profile) for p in qs]
        else:
            self.fields['profile'].choices = [('', 'Выберите профиль')]

        if profile_id and education_level:
            if education_level in ['бакалавриат', 'специалитет']:
                profile = BachSpecProfile.objects.filter(id=profile_id).first()
            elif education_level == 'магистратура':
                profile = MasterProfile.objects.filter(id=profile_id).first()
            elif education_level == 'аспирантура':
                profile = PhdProfile.objects.filter(id=profile_id).first()
            else:
                profile = None
            if profile:
                self.fields['education_form'].choices = [(
                    profile.education_form, profile.get_education_form_display()
                )]
            else:
                self.fields['education_form'].choices = [('', 'Выберите профиль')]
        else:
            self.fields['education_form'].choices = [('', 'Выберите профиль')]

    def initialize_dynamic_choices(self, data):
        # Факультеты
        faculties = Faculty.objects.all()
        self.fields['faculty'].choices = [('', 'Выберите факультет')] + [(f.id, f.name) for f in faculties]
        
        faculty_id = data.get('faculty')
        if isinstance(faculty_id, list):
            faculty_id = faculty_id[0] or faculty_id[-1]

        education_level = data.get('education_level')
        if education_level and faculty_id:
            if education_level in ['бакалавриат', 'специалитет']:
                qs = BachSpecDirection.objects.filter(faculty_id=faculty_id)
            elif education_level == 'магистратура':
                qs = MasterDirection.objects.filter(faculty_id=faculty_id)
            elif education_level == 'аспирантура':
                qs = PhdDirection.objects.filter(faculty_id=faculty_id)
            else:
                qs = []
            self.fields['direction'].choices = [('', 'Выберите направление')] + [(d.id, d.direction_name) for d in qs]

        direction_id = data.get('direction')
        if direction_id and education_level:
            if education_level in ['бакалавриат', 'специалитет']:
                qs = BachSpecProfile.objects.filter(direction_id=direction_id)
            elif education_level == 'магистратура':
                qs = MasterProfile.objects.filter(direction_id=direction_id)
            elif education_level == 'аспирантура':
                qs = PhdProfile.objects.filter(direction_id=direction_id)
            else:
                qs = []
            self.fields['profile'].choices = [('', 'Выберите профиль')] + [(p.id, p.profile) for p in qs]

        profile_id = data.get('profile')
        if profile_id and education_level:
            if education_level in ['бакалавриат', 'специалитет']:
                profile = BachSpecProfile.objects.filter(id=profile_id).first()
            elif education_level == 'магистратура':
                profile = MasterProfile.objects.filter(id=profile_id).first()
            elif education_level == 'аспирантура':
                profile = PhdProfile.objects.filter(id=profile_id).first()
            else:
                profile = None
            if profile:
                self.fields['education_form'].choices = [(profile.education_form, profile.get_education_form_display())]

    def get_direction_choices(self, instance):
            directions = []
            if instance.education_level in ('бакалавриат', 'специалитет'):
                qs = BachSpecDirection.objects.filter(faculty__name=instance.faculty)
                directions = [(d.id, d.direction_name) for d in qs]
            elif instance.education_level == 'магистратура':
                qs = MasterDirection.objects.filter(faculty__name=instance.faculty)
                directions = [(d.id, d.direction_name) for d in qs]
            elif instance.education_level == 'аспирантура':
                qs = PhdDirection.objects.filter(faculty__name=instance.faculty)
                directions = [(d.id, d.direction_name) for d in qs]
            return [('', 'Выберите направление')] + directions

    def get_profile_choices(self, instance):
            profiles = []
            if instance.education_level in ('бакалавриат', 'специалитет'):
                qs = BachSpecProfile.objects.filter(direction__id=instance.direction.id) if instance.direction else []
                profiles = [(p.id, p.profile) for p in qs]
            elif instance.education_level == 'магистратура':
                qs = MasterProfile.objects.filter(direction__id=instance.direction.id) if instance.direction else []
                profiles = [(p.id, p.profile) for p in qs]
            elif instance.education_level == 'аспирантура':
                qs = PhdProfile.objects.filter(direction__id=instance.direction.id) if instance.direction else []
                profiles = [(p.id, p.profile) for p in qs]
            return [('', 'Выберите профиль')] + profiles

    def get_education_form_choices(self, instance):
            if not instance.profile:
                return [('', 'Сначала выберите профиль')]
            form_choices = []
            if instance.education_level in ('бакалавриат', 'специалитет'):
                profile = BachSpecProfile.objects.filter(id=instance.profile.id).first()
            elif instance.education_level == 'магистратура':
                profile = MasterProfile.objects.filter(id=instance.profile.id).first()
            elif instance.education_level == 'аспирантура':
                profile = PhdProfile.objects.filter(id=instance.profile.id).first()
                
            if profile:
                return [(profile.education_form, profile.get_education_form_display())]
            return [('', 'Форма обучения не определена')]


class StaffEditForm(CommonProfileForm):
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше отчество',
            'class': 'patronymic',
            'autocomplete': 'new-password',
        }),
        label=''
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'Выберите дату рождения',
            'class': 'date-of-birth',
            'type': 'date',
        }),
        label='Дата рождения',
        input_formats=['%Y-%m-%d'],
    )

    role = forms.CharField( 
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите вашу роль',
            'class': 'role',
            'autocomplete': 'new-password',
        }),
        label='Роль'
    )
    class Meta(CommonProfileForm.Meta):
        model = Staff
        fields = CommonProfileForm.Meta.fields + ('patronymic', 'date_of_birth', 'role')
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        self.fields['faculty'].label_class = 'test-registration'


class GuestEditForm(forms.ModelForm):
    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше отчество',
            'class': 'patronymic',
            'autocomplete': 'new-password',
        }),
        label='Отчество',
        required=False
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'Выберите дату рождения',
            'class': 'date-of-birth',
            'type': 'date',
        }),
        label='Дата рождения',
        input_formats=['%Y-%m-%d'],
        required=False
    )
    role = forms.CharField(
        widget=forms.HiddenInput(),
        initial='Гость',
        label=''
    )
    class Meta:
        model = Guest
        fields = ('patronymic', 'date_of_birth', 'role')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'Гость'


class TestForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Название теста',
            'class': 'text-input-name-test',
        }),
        label='',
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Описание',
            'class': 'text-input-description-test',
        }),
        label='',
    )
    time = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'limited-time-input',
        }),
        required=False, 
        label='',
    )
    class Meta:
        model = Test
        fields = ['title', 'description', 'time', 'start_datetime']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'class': 'text-input-description-test'}),
        }


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Вопрос',
            'class': 'question-title-input',
        }),
        label='',
    )
    question_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'question-type-select',
            'autocomplete': 'new-password'
        }),
        label=''
    )
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'score']


class ScaleForm(forms.ModelForm):
    min_sign = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Подпись',
            'class': 'scale-label-input',
            'autocomplete': 'new-password'
        }),
        label=''
    )
    max_sign = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Подпись',
            'class': 'scale-label-input',
            'autocomplete': 'new-password'
        }),
        label=''
    )
    max_score = time = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': '10',
            'class': 'scale-number-input',
        }),
        label='',
    )
    class Meta:
        model = Scale
        fields = ['min_sign', 'max_sign', 'max_score']


class UserFieldsMixin(forms.ModelForm):
    first_name = forms.CharField(
        max_length=20, required=True, label="Имя"
    )
    last_name = forms.CharField(
        max_length=20, required=True, label="Фамилия"
    )
    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            
    def save_user_fields(self, user_instance):
        user_instance.first_name = self.cleaned_data['first_name']
        user_instance.last_name = self.cleaned_data['last_name']
        user_instance.save()


ROLE_CHOICES = (
    ('студент', 'Студент'),
    ('сотрудник', 'Сотрудник'),
    ('гость', 'Гость'),
)


class ProfileForm(forms.Form):
    last_name = forms.CharField(max_length=20, required=True, label="Фамилия")
    first_name = forms.CharField(max_length=20, required=True, label="Имя")
    patronymic = forms.CharField(max_length=200, required=False, label="Отчество")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Дата рождения")
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Роль")
    faculty = forms.CharField(max_length=200, required=False, label="Факультет")
    direction = forms.CharField(max_length=200, required=False, label="Направление")
    grade = forms.CharField(max_length=200, required=False, label="Курс")
    profile = forms.CharField(max_length=200, required=False, label="Профиль")
    study_form = forms.CharField(max_length=200, required=False, label="Форма обучения")
    education_level = forms.CharField(max_length=200, required=False, label="Уровень образования")

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)
        self.user_instance = user_instance

    def save(self, user):
        role = self.cleaned_data['role']
        if hasattr(user, 'student'):
            user.student.delete()
        if hasattr(user, 'staff'):
            user.staff.delete()
        if hasattr(user, 'guest'):
            user.guest.delete()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        common_kwargs = {
            'user': user,
            'date_of_birth': self.cleaned_data.get('date_of_birth'),
            'patronymic': self.cleaned_data.get('patronymic', '')
        }
        if role == 'студент':
            profile = Student.objects.create(
                role='Студент',
                faculty=self.cleaned_data.get('faculty', ''),
                direction=self.cleaned_data.get('direction', ''),
                grade=self.cleaned_data.get('grade', ''),
                profile=self.cleaned_data.get('profile', ''),
                study_form=self.cleaned_data.get('study_form', ''),
                education_level=self.cleaned_data.get('education_level', ''),
                **common_kwargs
            )
        elif role == 'сотрудник':
            profile = Staff.objects.create(
                role='Сотрудник',
                faculty=self.cleaned_data.get('faculty', ''),
                **common_kwargs
            )
        else:
            profile = Guest.objects.create(
                role='Гость',
                **common_kwargs
            )
        return profile

    def add_error(self, field, error):
        if field in self.errors:
            self.errors[field].append(error)
        else:
            self.errors[field] = [error]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == "студент":
            required_fields = ['faculty', 'direction', 'grade', 'profile', 'study_form', 'education_level']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'Укажите {self.fields[field].label.lower()}')
        elif role == "сотрудник":
            if not cleaned_data.get('faculty'):
                self.add_error('faculty', 'Укажите факультет')
