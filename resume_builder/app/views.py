from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ResumeForm, WorkExperienceForm, EducationForm, ProjectForm, \
    EmailForm, ProjectFormSet, WorkExperienceFormSet, EducationFormSet
from .models import CustomUser, Resume, WorkExperience, Education, Project
from allauth.account.views import LoginView, PasswordResetView, SignupView
from allauth.account.utils import complete_signup
from allauth.account.adapter import get_adapter
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.template import loader
from weasyprint import HTML
from django.core.cache import cache


@login_required
def index(request):
    return render(request, 'app/index.html')


@login_required
def create_resume(request):
    if request.method == 'POST':
        print(request.POST)
        resume_form = ResumeForm(request.POST)

        if resume_form.is_valid():

            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            work_experience_formset = WorkExperienceFormSet(request.POST, instance=resume)
            education_formset = EducationFormSet(request.POST, instance=resume)
            project_formset = ProjectFormSet(request.POST, instance=resume)

            if (work_experience_formset.is_valid() and
                    education_formset.is_valid() and project_formset.is_valid()):
                work_experience_formset.save()
                education_formset.save()
                project_formset.save()

                return redirect(reverse_lazy('app:resume', args=[resume.id]))
        else:
            print('Ошибки:', resume_form.errors)
            print(work_experience_formset.errors)
            print(education_formset.errors)
            print(project_formset.errors)
    else:
        resume_form = ResumeForm()
        work_experience_formset = WorkExperienceFormSet(instance=None)
        education_formset = EducationFormSet(instance=None)
        project_formset = ProjectFormSet(instance=None)

    context = {
        'resume_form': resume_form,
        'work_experience_formset': work_experience_formset,
        'education_formset': education_formset,
        'project_formset': project_formset,
    }
    return render(request, 'app/create-resume.html', context)


@login_required
def resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    skills = [skill for skill in resume.skills.split(',')]
    return render(request, 'app/resume.html', {'resume': resume,
                                               'skills': skills})


# создание pdf файла из html страницы с резюме
def resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    skills = [skill for skill in resume.skills.split(',')]
    cache_key = f'resume_{resume_id}'

    html_content = cache.get(cache_key)

    if not html_content: 
        template = loader.get_template('app/resume_pdf.html')
        html_content = template.render({'resume': resume, 'skills': skills})  
        cache.set(cache_key, html_content, timeout=60 * 30) # кэширование на 30 минут

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response


# AUTH
def first_page_login(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid(): 
            email = form.cleaned_data['email']
            User = get_user_model()  # Получаем модель пользователя

            try:
                user = User.objects.get(email=email)
                # Проверяем, зарегистрирован ли пользователь через социальную сеть
                if user.social_auth.exists():
                    email_address = EmailAddress.objects.filter(user=user, email=email, verified=True).first()
                    if email_address:
                        return redirect(f"{reverse('account_login')}?email={email}")
                    else:
                        return redirect('password_reset_notification')
                return redirect(f"{reverse('account_login')}?email={email}")
            
            except User.DoesNotExist:
                error_message = 'Пользователь с таким email не найден'
                form.add_error('email', error_message)
    else:
        form = EmailForm()

    return render(request, 'account/first_page_login.html', {'form': form})


def password_reset_notification(request):
    return render(request, 'account/password_reset_notification.html')


class CustomLoginView(LoginView):  # переопределение представления входа (теперь email сохраняется в форме даже при ошибке)
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', '')
        context = self.get_context_data()
        context['email'] = email
        return self.render_to_response(context)
    
    def form_invalid(self, form):
        email = self.request.POST.get('login', '')
        return self.render_to_response(self.get_context_data(form=form, email=email))
    
    def form_valid(self, form):
        email = form.cleaned_data.get('login') 
        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            messages.error(self.request, "Пользователь с указанным email не найден.")
            return self.form_invalid(form)
        
        email_address = EmailAddress.objects.filter(email=email, verified=True).first()
        
        if email_address is None:
            messages.error(self.request, "Ваш email еще не подтвержден. Проверьте вашу почту.")
            return redirect('account_email_verification_sent')

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):  # переопределение представления входа (теперь email сохраняется в форме даже при ошибке)
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', '')
        context = self.get_context_data()
        context['email'] = email
        return self.render_to_response(context)

    def form_invalid(self, form):
        email = self.request.POST.get('email', '')
        return self.render_to_response(self.get_context_data(form=form, email=email))
    