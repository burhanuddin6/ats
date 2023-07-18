from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from . import forms as a_forms
from . import email
from . import helpers as a_helpers
from . import models as a_models
# Create your views here.

def index(request):
    # If user is not a candidate, show all jobs
    if not a_helpers.is_candidate(request.user):
        if "job_id" in request.session:
            del request.session['job_id']
        return HttpResponseRedirect(reverse('applicants:all_jobs'))
     
    if a_helpers.candidate_has_application(candidate=request.user.candidate):
        return HttpResponse("From index: You have already applied to a job.")
    
    if "job_id" in request.session: # divert to that job
        return HttpResponseRedirect(reverse('applicants:job', 
                                            args=(request.session['job_id'],)))
    # show all jobs
    return HttpResponseRedirect(reverse('applicants:all_jobs'))
    
def login_view(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('applicants:index'))
        else:
            return render(request, 'applicants/login.html', {
                'login_form': a_forms.LoginForm(),
                'message': "Invalid credentials"
            })
    messages.info(request, "Please login")
    if request.method == "GET":
        return render(request, 'applicants/login.html', {
            'login_form': a_forms.LoginForm(),
        })

def logout_view(request):
    logout(request)
    return render(request, 'applicants/login.html', {
        'login_form': a_forms.LoginForm(),
        'message': "Logged out",
    })

def signup(request):
    if request.method == 'POST':
        if 'candidate_form' in request.POST:
            candidate_form = a_forms.SignUpForm(request.POST)
            if candidate_form.is_valid():
                cleaned_data = candidate_form.cleaned_data
                request.session['candidate_form'] = cleaned_data
                request.session['verification_code'] = a_helpers.generate_numeric_string(6)
                email.send_verification_email(
                    candidate_form.cleaned_data['email'], 
                    request.session['verification_code'])
                return HttpResponseRedirect(reverse('applicants:verify'))
            
            messages.error(request, "Invalid form")
            return render(request, 'applicants/signup.html', {
                'candidate_form': candidate_form
            })
        
        # There is no other form
        raise a_helpers.InvalidFormException("There is no other form")
        
    # request method is GET or the above failed
    if request.method == "GET":
        messages.info(request, "Please Sign Up")
        return render(request, 'applicants/signup.html', {
            'candidate_form': a_forms.SignUpForm(),
        })

def verify(request):
    if request.method == "POST":
        verify_form = a_forms.VerifyForm(request.POST)
        if verify_form.is_valid():
            if verify_form.cleaned_data['verification_code'] == request.session['verification_code']: #pylint: disable=line-too-long
                # create user-candidate
                a_helpers.create_candidate(
                    email=request.session['candidate_form']['email'],
                    password=request.session['candidate_form']['password'],
                    first_Name=request.session['candidate_form']['first_Name'],
                    last_Name=request.session['candidate_form']['last_Name']
                )
                messages.success(request, "Account created successfully. Please login.")
                return HttpResponseRedirect(reverse('applicants:login'))
        else:
            return render(request, 'applicants/verify.html', {
                'verify_form': verify_form,
                'error': "The code you entered is incorrect. Please try again."
            })
    ####################
    # create_candidate(
    #     email=request.session['candidate_form']['email'],
    #     password=request.session['candidate_form']['password'],
    #     first_Name=request.session['candidate_form']['first_Name'],
    #     last_Name=request.session['candidate_form']['last_Name']
    # )
    # messages.success(request, "Account created successfully. Please login.")
    # return HttpResponseRedirect(reverse('applicants:login'))
    #########################
    messages.info(request, "Please verify your email")
    if request.method == "GET":
        return render(request, 'applicants/verify.html', {
            'verify_form': a_forms.VerifyForm()
        })

def success(request):
    return HttpResponse("Success!")


def all_jobs_view(request):
    return render(request, 'applicants/all_jobs.html',{
        'jobs': a_models.Job.objects.all()
    })

def job_view(request, job_id):
    job = a_models.Job.objects.get(pk=job_id)
    return render(request, 'applicants/job.html', {
        'job_fields': job._meta.get_fields(),
        'job': job,
        'application': a_models.Application.objects.filter(job_ID=job).first(),
    })

def apply_for_job(request, job_id):
    if request.method == "GET":
        request.session['job_id'] = job_id
        # check if user is a candidate
        if not a_helpers.is_candidate(request.user):
            return HttpResponseRedirect(reverse('applicants:signup'))
        
        return HttpResponseRedirect(reverse('applicants:application', 
                                                    args=(request.user.candidate.candidate_ID,)))

    if request.method == "POST":
        raise NotImplementedError("method POST NOT implemented for view: apply_for_job")


def application(request, applicant_id):
    if request.method == "POST":
        saved_success, forms_dict = a_helpers.save_application_data(
            request, 
            applicant_id, 
            request.session['job_id']
        )

        if saved_success:
            return HttpResponse("Application saved successfully.")
        
        forms_dict['applicant'] = a_models.Candidate.objects.get(pk=applicant_id)
        forms_dict['user'] = request.user
        forms_dict['applicant_id'] = applicant_id
        return render(request, 'applicants/application_ai_gen.html', forms_dict)
    if request.method == "GET":
        for form in a_forms.CandidateReferencesFormSet(
                queryset=a_models.Reference.objects.none(),
                prefix='references'):
            print(form.prefix)
        return render(request, 'applicants/application_ai_gen.html', {
            'user': request.user,
            'applicant': a_models.Candidate.objects.get(pk=applicant_id),
            'applicant_id': applicant_id,
            'profile_form': a_forms.CandidateProfileForm(),
            'education_form': a_forms.CandidateEducationForm(),
            'experience_form': a_forms.CandidateExperienceForm(),
            'skills_formset': a_forms.CandidateSkillsFormSet(
                queryset=a_models.Skill.objects.none(),
                prefix='skills'
            ),
            'references_formset': a_forms.CandidateReferencesFormSet(
                queryset=a_models.Reference.objects.none(),
                prefix='references'
            ),
        })


def profile(request):
    user = request.user
    if request.method == "GET":
        return render(request, 'applicants/profile.html', {
            'user': user,
            # 'notifications': Notification.objects.filter(user=user),
        })
        
def xyz(request):
    return render(request=request, template_name='applicants/abc.html', context={
        "form": a_forms.LoginForm(),
        "file": "file.pdf"
    })
