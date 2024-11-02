from django import forms 
from allauth.account.forms import SignupForm
from .models import Resume, WorkExperience, Education, Project
from django.core.validators import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet


# формы для резюме
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['fullname', 'skills', 'years_of_work', 'position', 'email', 'about', 'phone_number',
                   'github', 'telegram', 'vk', 'linkedIn']
        widgets = {
            'fullname': forms.TextInput(attrs={'placeholder': 'Введите ваше полное имя (Иванов Иван Иванович)'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Введите ваши навыки через запятую'}),
            'years_of_work': forms.TextInput(attrs={'placeholder': 'Введите количество лет опыта (X года X месяцев))', 'type': 'text'}),
            'position': forms.TextInput(attrs={'placeholder': 'Введите желаемую должность'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите ваш Email'}),
            'about': forms.Textarea(attrs={'placeholder': 'Кратко опишите себя, свой опыт и др.'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Номер: +79991234567 или 89991234567', 'type': 'tel'}),
            'github': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш GitHub', 'type': 'url'}),
            'telegram': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш Telegram', 'type': 'url'}),
            'vk': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш VK', 'type': 'url'}),
            'linkedIn': forms.URLInput(attrs={'placeholder': 'Введите ссылку на ваш LinkedIn', 'type': 'url'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'position', 'start_date', 'end_date', 'work_description']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Введите название компании'}),
            'position': forms.TextInput(attrs={'placeholder': 'Введите вашу должность'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Введите дату устройства (Сентябрь 2024)', 'type': "month"}),
            'end_date': forms.TextInput(attrs={'placeholder': 'Введите дату устройства (Октябрь 2024)', 'type': "month"}),
            'work_description': forms.Textarea(attrs={'placeholder': 'Введите описание вашей работы'}),
        }
        
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution_name', 'faculty', 'degree', 'start_date', 'end_date']
        widgets = {
            'institution_name': forms.TextInput(attrs={'placeholder': 'Введите название учебного заведения'}),
            'faculty': forms.TextInput(attrs={'placeholder': 'Введите название факультета'}),
            'degree': forms.TextInput(attrs={'placeholder': 'Введите степень (например, Бакалавр, Магистр)'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Введите год начала обучения (YYYY)', 'type': 'number'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'Введите год окончания обучения (YYYY)', 'type': 'number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Год начала обучения не может быть больше года окончания')
        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'technologies_used', 'github_link']
        widgets = {
            'project_name': forms.TextInput(attrs={'placeholder': 'Введите название проекта'}),
            'project_description': forms.Textarea(attrs={'placeholder': 'Введите описание проекта'}),
            'technologies_used': forms.Textarea(attrs={'placeholder': 'Введите используемые технологии'}),
            'github_link': forms.TextInput(attrs={'placeholder': 'Введите ссылку на GitHub (если есть)', 'type': 'url'}),
        }
    
    
# формсеты для добавления форм
class BaseWorkExperienceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if self.total_form_count() > 5:
            raise ValidationError("Можно добавить не более 5 форм опыта работы.")

class BaseEducationFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if self.total_form_count() > 3:
            raise ValidationError("Можно добавить не более 3 форм опыта работы.")

class BaseProjectFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if self.total_form_count() > 3:
            raise ValidationError("Можно добавить не более 3 форм опыта работы.")


WorkExperienceFormSet = inlineformset_factory(
    Resume,
    WorkExperience,
    form=WorkExperienceForm,
    formset=BaseWorkExperienceFormSet,
    extra=0,
    can_delete=False,
    max_num=5,
)

EducationFormSet = inlineformset_factory(
    Resume,
    Education,
    form=EducationForm,
    formset=BaseEducationFormSet,
    extra=0,
    can_delete=False,
    max_num=3,
)

ProjectFormSet = inlineformset_factory(
    Resume,
    Project,
    form=ProjectForm,
    formset=BaseProjectFormSet,
    extra=0,
    can_delete=False,
    max_num=3,
)


# auth
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=150, label='Ваше имя')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError("Введите ваше имя.")

        return username
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.username = self.cleaned_data['username']
        user.save()
        return user
    

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
