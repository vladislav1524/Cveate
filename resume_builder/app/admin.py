from django.contrib import admin
from .models import Resume, WorkExperience, Education, Project, CustomUser


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1 

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'position', 'start_date', 'end_date', 'work_description')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'skills', 'email', 'phone_number',
                     'github', 'telegram', 'vk', 'linkedIn')
    inlines = [WorkExperienceInline, EducationInline, ProjectInline]
    