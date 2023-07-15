from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django import template
from django.utils import timezone

from applicants import models as a_models
from applicants import helpers as a_helpers

from . import forms as r_forms
from . import helpers as r_helpers

register = template.Library()

DAYS_OF_WEEK = {
    0: 'M',
    1: 'T',
    2: 'W',
    3: 'H',
    4: 'F',
    5: 'S',
    6: 'U'
}

# Create your views here.
def index(request):
    if request.user.is_authenticated and a_helpers.is_recruiter(request.user):
        return HttpResponseRedirect(reverse('recruiters:dashboard'))
    else:
        messages.info(request, "Please login")
        return HttpResponseRedirect(reverse('recruiters:login'))

def login_view(request):
    print(a_helpers.is_recruiter(request.user))
    if request.method == "POST":
        login_form = r_forms.LoginForm(request.POST)
        if not login_form.is_valid():
            return render(request, 'recruiters/login.html', {
                'login_form': r_forms.LoginForm(),
                'message': "Invalid credentials"
            })
        print(login_form.cleaned_data)
        user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
        if user is not None:
            if not a_helpers.is_recruiter(user):
                return render(request, 'recruiters/login.html', {
                    'login_form': r_forms.LoginForm(),
                    'message': "You are not a recruiter"
                })
            login(request, user)
            messages.success(request, f"Welcome back {user.recruiter.first_Name}!")
            return HttpResponseRedirect(reverse('recruiters:index'))
        else:
            return render(request, 'recruiters/login.html', {
                'login_form': r_forms.LoginForm(),
                'message': "Invalid credentials"
            })
    if request.method == "GET":
        return render(request, 'recruiters/login.html', {
            'login_form': r_forms.LoginForm(),
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('recruiters:index'))

def get_user_messages(request):
    return render(request, 'recruiters/div_messages.html', {})

SEARCH_TYPES = {
    'name':{'value': 1, 'verbose_name': 'Name'},
    'skills':{'value': 2, 'verbose_name': 'Skills'},
    'experience':{'value': 3, 'verbose_name': 'Past Company'},
    'education':{'value': 4, 'verbose_name': 'Education'},
    'job_applied':{'value': 5, 'verbose_name': 'Job Applied'},
}
@login_required
@user_passes_test(a_helpers.is_recruiter)
def dashboard(request):
    return render(request, 'recruiters/dashboard.html', {
        'heading': 'Dashboard',
        'user': request.user,
        'candidates': a_models.Candidate.objects.all(),
        'search_types': SEARCH_TYPES.values(),
        'email_form': r_forms.EmailCandidateForm(),
    })


@login_required
@user_passes_test(a_helpers.is_recruiter)
def candidates(request):
    return render(request, 'recruiters/candidates.html', {
        'heading': 'Candidates',
        'user': request.user,
        'candidates': a_models.Candidate.objects.all(),
    })


@login_required
@user_passes_test(a_helpers.is_recruiter)
def jobs(request):
    return render(request, 'recruiters/jobs.html', {
        'heading': 'Jobs',
        'user': request.user,
        'jobs': a_models.Job.objects.all(),
    })


@login_required
@user_passes_test(a_helpers.is_recruiter)
def job(request, job_id):
    active_stage_id = request.GET.get('stage_id', None)
    active_stage_name = request.GET.get('stage_name', "application")
    context = r_helpers.get_job_context(int(job_id), active_stage_id, active_stage_name)
    return render(request, 'recruiters/job.html', context=context)

@login_required
@user_passes_test(a_helpers.is_recruiter)
def approve_candidate(request, job_id):
    """
    TODO if there exist a next stage then add candidate to that row with undecided status
    """
    response = JsonResponse({})
    if r_helpers.is_ajax(request):
        try:
            r_helpers.change_candidate_status(
                candidate_id=request.GET.get('candidate_id', None), 
                stage_id=request.GET.get('stage_id', None), 
                stage_name=request.GET.get('stage_name', None), 
                new_status=a_models.Candidate_Application.ACCEPTED
                )
            r_helpers.add_candidate_to_next_stage(
                candidate_id=request.GET.get('candidate_id', None),
                current_stage_id=request.GET.get('stage_id', None),
                current_stage_name=request.GET.get('stage_name', None),
                )
        except Exception as e:
            print(e)
            response.status_code = 400
    else:
        response.status_code = 400
    return response

@login_required
@user_passes_test(a_helpers.is_recruiter)
def reject_candidate(request, job_id):
    """ TODO if there exist a next stage then add candidate to that row with undecided status
    """
    response = JsonResponse({})
    if r_helpers.is_ajax(request):
        # try:
        r_helpers.drop_candidate_from_stage(
            job_id=job_id,
            candidate_id=request.GET.get('candidate_id', None), 
            stage_id=request.GET.get('stage_id', None), 
            stage_name=request.GET.get('stage_name', None)
            )
        # except:
        #     response.status_code = 400
    else:
        response.status_code = 400
    return response


@login_required
@user_passes_test(a_helpers.is_recruiter)
def create_job(request):
    if request.method == "POST":
        try:
            r_helpers.create_job(request)
            return HttpResponseRedirect(reverse('recruiters:jobs'))
        except Exception as e:
            messages.error(request, "Error creating job. Invalid data")
            return render(request, 'recruiters/create_job.html', {
                'heading': 'Create Job',
                'user': request.user,
                'job_form': r_forms.JobCreationForm(),
                'application_form': r_forms.JobApplicationForm(),
            })
    form = r_forms.JobCreationForm()
    print(form.fields['description'].widget.__class__.__name__) 
    if request.method == "GET":
        return render(request, 'recruiters/create_job.html', {
            'heading': 'Create Job',
            'user': request.user,
            'job_form': r_forms.JobCreationForm(),
            'application_form': r_forms.JobApplicationForm(),
        })
    
@login_required
@user_passes_test(a_helpers.is_recruiter)
def create_stage(request, job_id, stage_name):
    job = a_models.Job.objects.get(id=job_id)
    if request.method == "POST":
        if stage_name == "interview":
            form = r_forms.JobInterviewForm(request.POST)
        elif stage_name == "test":
            form = r_forms.JobInterviewForm(request.POST)
        no_overlaps = True
        if form.is_valid():
            no_overlaps, overlapping_stage, min_date = r_helpers.check_stage_overlap(job_id, form.cleaned_data['start_Date'], form.cleaned_data['end_Date'], stage_name)
            if no_overlaps:
                form = form.save(commit=False)
                form.job_ID = job
                form.created_By = request.user.recruiter
                form.save()
                return HttpResponseRedirect(reverse('recruiters:job', kwargs={'job_id': job_id}))   
        if not no_overlaps:
            messages.error(request, "Error creating stage. Stage overlaps with {}. Date must be greater than {}".format(overlapping_stage, min_date))
        # add form error messages
        return render(request, 'recruiters/create_interview_stage.html', {
            'heading': 'Create Interview Stage',
            'user': request.user,
            'stage_form': form,
            'job': job,
        })
    else:
        if stage_name == "interview":
            new_form = r_forms.JobInterviewForm()
        elif stage_name == "test":
            new_form = r_forms.JobInterviewForm()
        return render(request, 'recruiters/create_interview_stage.html', {
            'heading': 'Create Interview Stage',
            'user': request.user,
            'stage_form': new_form,
            'job': job,
        })

@login_required
@user_passes_test(a_helpers.is_recruiter)
def search_candidates(request):
    candidates = []
    try:
        candidates = r_helpers.search_candidates(request, SEARCH_TYPES=SEARCH_TYPES)
    except Exception as e:
        print(e)
    return render(request, 'recruiters/div_candidates.html', {
        'candidates': candidates,
    })

def create_interview_slots(request, job_id, stage_id):
    job = a_models.Job.objects.get(id=job_id)
    if request.method == "POST":
        slot_group_form = r_forms.InterviewSlotGroupForm(request.POST)
        print(request.POST)
        interview_daily_forms = [
            r_forms.InterviewDailyTimeForm(request.POST, prefix=str(x)) for x in range(0,7)
        ]
        print(interview_daily_forms)
        if slot_group_form.is_valid() and all([form.is_valid() for form in interview_daily_forms]):
            slot_group_form = slot_group_form.save(commit=False)
            slot_group_form.interview_ID = a_models.Interview.objects.get(id=stage_id)
            slot_group_form.save()
            for form in interview_daily_forms:
                if form.cleaned_data['check']:
                    form = form.save(commit=False)
                    form.slot_Group_ID = slot_group_form
                    form.save()
            return HttpResponseRedirect(reverse('recruiters:job', kwargs={'job_id': job_id}))
        else:
            messages.error(request, "Error creating interview slots. Invalid data")
            return render(request, 'recruiters/create_interview_slots.html', {
                'heading': job.title,
                'sub_heading': 'Create Interview Slots',
                'user': request.user,
                'job': job,
                'stage': a_models.Interview.objects.get(id=stage_id),
                'slot_group_form': slot_group_form,
                'interview_daily_forms': interview_daily_forms,
            })
    else:
        return render(request, 'recruiters/create_interview_slots.html', {
            'heading': job.title,
            'sub_heading': 'Create Interview Slots',
            'user': request.user,
            'job': job,
            'stage': a_models.Interview.objects.get(id=stage_id),
            'slot_group_form': r_forms.InterviewSlotGroupForm(),
            'interview_daily_forms': [ 
                r_forms.InterviewDailyTimeForm(
                    initial={'day': value, 'check':True, 'start_Time': '09:00', 'end_Time': '17:00'}, 
                    prefix=str(i)
                )
                for i, value in enumerate(DAYS_OF_WEEK)
            ],
        })
    
@login_required
@user_passes_test(a_helpers.is_recruiter)
def schedule_candidate_interview(request, candidate_id, stage_id):
    """Takes in a candidate and an interview stage, checks if there is an available slot,
    if not then alerts the user that no slots are available for the given interview stage.
    If slot is available, then assigns that slot to the given candidate.

    Args:
        request (object): HttpRequest
        candidate_id (int): candidate id to get the candidate
        stage_id (int): interview stage id
    """
    response = JsonResponse({})
    try:
        candidate_interview = a_models.Candidate_Interview.objects.get(candidate_ID=candidate_id, interview_ID=stage_id)
        slot = a_models.Interview_Slot.objects.filter(slot_Group_ID__interview_ID=stage_id, vacant=True, datetime_Of_Interview__gt=(timezone.now() + timezone.timedelta(days=1))).order_by('datetime_Of_Interview').first()
        assert r_helpers.not_none(slot, candidate_interview)
    except Exception as e:
        print(e)
        if e.__class__.__name__ == "AssertionError":
            messages.error(request, "No slots available for this interview.\nPlease create a slot first.")
        else:
            messages.error(request, "Internal Server Error: Error scheduling candidate.\nPlease Try Again")
        response.status_code = 500
        return response
    try:
        if candidate_interview.interview_Slot_ID is not None:
            prev_slot = candidate_interview.interview_Slot_ID
            prev_slot.delete()
        candidate_interview.interview_Slot_ID = slot
        slot.vacant = False
        candidate_interview.save(update_fields=['interview_Slot_ID'])
        slot.save(update_fields=['vacant'])
    except Exception as e:
        print(e)
        slot.vacant = True
        candidate_interview.interview_Slot_ID = None
        candidate_interview.save(update_fields=['interview_Slot_ID'])
        slot.save(update_fields=['vacant'])
        messages.error(request, "Could not schedule the candidate. Please Try Again")
        response.status_code = 400
        return response
    messages.success(request, "Candidate scheduled successfully")
    return response


@login_required
@user_passes_test(a_helpers.is_recruiter)    
def delete_candidate_interview(request, candidate_id, stage_id):
    """Deletes an interview slot

    Args:
        request (object): HttpRequest
        slot_id (int): interview slot id
    """
    response = JsonResponse({})
    try:
        candidate_interview = a_models.Candidate_Interview.objects.get(candidate_ID=candidate_id, interview_ID=stage_id)
        candidate_interview.interview_Slot_ID.delete()
    except Exception as e:
        print(e)
        messages.error(request, "Could not delete the slot. Please Try Again")
        response.status_code = 400
        return response
    messages.success(request, "Candidate Interview deleted successfully")
    return response

def get_div_job_candidates(request, job_id):
    """Returns the div containing the candidates for a given job

    Args:
        request (object): HttpRequest
    """
    active_stage_id = request.GET.get('active_stage_id', None)
    active_stage_name = request.GET.get('active_stage_name', None)
    assert r_helpers.not_none(active_stage_id, active_stage_name)
    context = r_helpers.get_job_context(int(job_id), active_stage_id, active_stage_name)
    print("div_job_was called")
    return render(request, 'recruiters/div_job_candidates.html', {
        'job': job,
        'active_stage_id': active_stage_id,
        'active_stage_name': active_stage_name,
        'accepted_candidates': context['accepted_candidates'],
        'rejected_candidates': context['rejected_candidates'],
        'undecided_candidates': context['undecided_candidates'],
    })
