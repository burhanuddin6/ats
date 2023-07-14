from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from .helpers import *
from django.contrib import messages
# Create your views here.

def index(request):
    # If user is not a candidate, show all jobs
    if not is_candidate(request.user):
        if "job_id" in request.session:
            del request.session['job_id']
        return HttpResponseRedirect(reverse('applicants:all_jobs'))
    else: 
        if candidate_has_application(candidate=request.user.candidate):
            return HttpResponse("From index: You have already applied to a job.")
        else:
            if "job_id" in request.session: # divert to that job
                return HttpResponseRedirect(reverse('applicants:job', args=(request.session['job_id'],)))
            else: # show all jobs
                return HttpResponseRedirect(reverse('applicants:all_jobs'))
    
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('applicants:index'))
        else:
            return render(request, 'applicants/login.html', {
                'login_form': LoginForm(),
                'message': "Invalid credentials"
            })
    messages.info(request, "Please login")
    if request.method == "GET":
        return render(request, 'applicants/login.html', {
            'login_form': LoginForm(),
        })

def logout_view(request):
    logout(request)
    return render(request, 'applicants/login.html', {
        'login_form': LoginForm(),
        'message': "Logged out",
    })

def signup(request):
    if request.method == 'POST':
        if 'candidate_form' in request.POST:
            candidate_form = CandidateForm(request.POST)
            if candidate_form.is_valid():
                cleaned_data = candidate_form.cleaned_data
                request.session['candidate_form'] = cleaned_data
                request.session['verification_code'] = generate_numeric_string(6)
                email.send_verification_email(candidate_form.cleaned_data['email'], request.session['verification_code'])
                return HttpResponseRedirect(reverse('applicants:verify'))
            else:
                messages.error(request, "Invalid form")
                return render(request, 'applicants/signup.html', {
                    'candidate_form': candidate_form
                })
        else:
            # There is no other form
            raise Exception("Invalid form")
        
    # request method is GET or the above failed
    if request.method == "GET":
        messages.info(request, "Please Sign Up")
        return render(request, 'applicants/signup.html', {
            'candidate_form': CandidateForm(),
        })

def verify(request):
    if request.method == "POST":
        verify_form = VerifyForm(request.POST)
        if verify_form.is_valid():
            if verify_form.cleaned_data['verification_code'] == request.session['verification_code']:
                # create user-candidate
                create_candidate(
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
            'verify_form': VerifyForm()
        })

def success(request):
    return HttpResponse("Success!")


def all_jobs_view(request):
    return render(request, 'applicants/all_jobs.html',{
        'jobs': Job.objects.all()
    })

def job_view(request, job_id):
    job = Job.objects.get(pk=job_id)
    return render(request, 'applicants/job.html', {
        'job_fields': job._meta.get_fields(),
        'job': job,
        'application': Application.objects.filter(job_ID=job).first(),
    })

def apply_for_job(request, job_id):
    if request.method == "GET":
        request.session['job_id'] = job_id
        # check if user is a candidate
        if not is_candidate(request.user):
            return HttpResponseRedirect(reverse('applicants:signup'))
        else:
            return HttpResponseRedirect(reverse('applicants:application', args=(request.user.candidate.candidate_ID,)))
    
    if request.method == "POST":
        raise Exception("method POST NOT implemented for view: apply_for_job")
    
def application(request, applicant_id):
    if request.method == "POST":
        save_application_data(request, applicant_id, request.session['job_id'])
        return HttpResponse("Application saved successfully.")
    if request.method == "GET":
        for form in CandidateReferencesFormSet(
                queryset=Reference.objects.none(),
                prefix='references'):
            print(form.prefix)
        return render(request, 'applicants/application_ai_gen.html', {
            'user': request.user,
            'applicant': Candidate.objects.get(pk=applicant_id),
            'applicant_id': applicant_id,
            'profile_form': CandidateProfileForm(),
            'education_form': CandidateEducationForm(),
            'experience_form': CandidateExperienceForm(),
            'skills_formset': CandidateSkillsFormSet(
                queryset=Skill.objects.none(),
                prefix='skills'
            ),
            'references_formset': CandidateReferencesFormSet(
                queryset=Reference.objects.none(),
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
        "form": LoginForm(),
        "file": "file.pdf"
    })
