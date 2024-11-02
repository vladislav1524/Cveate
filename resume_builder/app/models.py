from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from month.models import MonthField
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        
        existing_user = self.model.objects.filter(email=email).first()
        if existing_user:
            for key, value in extra_fields.items():
                setattr(existing_user, key, value)
            existing_user.save(using=self._db)
            return existing_user
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, verbose_name='именем', unique=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.email



class Resume(models.Model):
    user = models.ForeignKey(CustomUser, related_name='resumes', on_delete=models.CASCADE, db_index=True)
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    skills = models.TextField(verbose_name='Ваши технологии')
    years_of_work = models.CharField(verbose_name='Опыт работы', max_length=50)
    position = models.CharField(verbose_name='Желаемая должность', max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^(?:\+7|8)\d{10}$',
                                  message="Номер телефона должен быть введен в формате: \
                                    '+79991234567' или '89991234567'. Должно быть 10 цифр после кода.")
    about = models.TextField(verbose_name='О себе', max_length=700, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True, verbose_name='Номер телефона')
    github = models.URLField(verbose_name='Ссылка на GitHub', blank=True)
    telegram = models.URLField(verbose_name='Ссылка на Telegram', blank=True, null=True)
    vk = models.URLField(verbose_name='Ссылка на vk', blank=True)
    linkedIn = models.URLField(verbose_name='Ссылка на linkedIn', blank=True, null=True)

    class Meta:
        verbose_name = 'резюме'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, related_name='work_experiences', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, verbose_name='Название организации', blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name='Позиция', blank=True, null=True)
    start_date = MonthField(verbose_name='Дата устроства', blank=True, null=True)
    end_date = MonthField(verbose_name='Дата ухода (если есть)', blank=True, null=True)
    work_description = models.TextField(verbose_name='Описание работы', blank=True, null=True)

    months_ru = [
        "", "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ]

    def formatted_dates(self):
        start = f"{self.months_ru[self.start_date.month]} {self.start_date.year}" if self.start_date else 'Не указано'
        end = f"{self.months_ru[self.end_date.month]} {self.end_date.year}" if self.end_date else 'по настоящее время'

        return f"{start} - {end}"


class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='educations', on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=255,
                                         verbose_name='Название учебного заведения (если есть)',
                                           blank=True, null=True)
    faculty = models.CharField(max_length=25, verbose_name='Факультет/название курса', blank=True, null=True)
    degree = models.CharField(max_length=255, verbose_name='Степень (если это вуз)',
                               blank=True, null=True)
    start_date = models.PositiveIntegerField(verbose_name='Год поступления', blank=True, null=True)
    end_date = models.PositiveIntegerField(verbose_name='Год окончания обучения', blank=True, null=True)

    def formatted_dates(self):
        start = self.start_date if self.start_date else 'Не указано'
        end = self.end_date if self.end_date else 'по настоящее время'

        return f"{start} - {end}"
    

class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name='projects', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255, verbose_name='Название проекта',
                                     blank=True, null=True)
    project_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    technologies_used = models.TextField(verbose_name='Использованные технологии и решения', blank=True, null=True)
    github_link = models.URLField(verbose_name='ссылка на репозиторий github', blank=True, null=True)
