from applicants import models as a_models
from recruiters import forms as r_forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
# validationerror
from django.core.exceptions import ValidationError

def not_none(*args):
    return all([x is not None for x in args])

def check_stage_overlap(job_id, start_Date, end_Date, stage_name):
    job = a_models.Job.objects.get(pk=job_id)
    stages = list(a_models.Base_Job_Stage.objects.filter(job_ID=job_id).order_by('end_Date'))
    for stage in stages:
        print(stage)
    if stage_name.lower() == "application" and job.job_stages.filter(name="Application").exists():
        return (False, "Application", "")
    if (stages[-1].end_Date > start_Date or stages[-1].end_Date > end_Date):
        return (False, stages[-1].name, stages[-1].end_Date)
    return (True, "", "")

def get_job_context(job_id, stage_id, stage_name):

    job = a_models.Job.objects.get(pk=job_id)
    stages = { 'application': [job], 'test': list(a_models.Test.objects.filter(job_ID=job).order_by('start_Date')), 'interview': list(a_models.Interview.objects.filter(job_ID=job).order_by('start_Date'))}
    
    if stage_name.lower() == "application":
        # stage = a_models.Application.objects.get(pk=stage_id)
        if stage_id is None:
            stage_id = a_models.Application.objects.get(job_ID=job).pk
        undecided_candidates = a_models.Candidate.objects.filter(
            candidate_application__in = # related name of candidate in Job_Application
            a_models.Candidate_Application.objects.filter(application_ID=stage_id).filter(status=a_models.Candidate_Application.UNDECIDED)
            )
        rejected_candidates = a_models.Candidate.objects.filter(
            candidate_application__in = # related name of candidate in Job_Application
            a_models.Candidate_Application.objects.filter(application_ID=stage_id).filter(status=a_models.Candidate_Application.REJECTED)
            )
        accepted_candidates = a_models.Candidate.objects.filter(
            candidate_application__in = # related name of candidate in Job_Application
            a_models.Candidate_Application.objects.filter(application_ID=stage_id).filter(status=a_models.Candidate_Application.ACCEPTED)
            )
    elif stage_name.lower() == "test":
        undecided_candidates = a_models.Candidate.objects.filter(
            candidate_tests__in = # related name of candidate in Candidate_Test
            a_models.Candidate_Test.objects.filter(test_ID=stage_id).filter(status=a_models.Candidate_Test.UNDECIDED)
            )
        rejected_candidates = a_models.Candidate.objects.filter(
            candidate_tests__in = # related name of candidate in Candidate_Test
            a_models.Candidate_Test.objects.filter(test_ID=stage_id).filter(status=a_models.Candidate_Test.REJECTED)
            )
        accepted_candidates = a_models.Candidate.objects.filter(
            candidate_tests__in = # related name of candidate in Candidate_Test
            a_models.Candidate_Test.objects.filter(test_ID=stage_id).filter(status=a_models.Candidate_Test.ACCEPTED)
            )
    elif stage_name.lower() == "interview":
        undecided_candidates = a_models.Candidate.objects.filter(
            interviews__in = # related name of candidate in Candidate_Interview 
            a_models.Candidate_Interview.objects.filter(interview_ID=stage_id).filter(status=a_models.Candidate_Interview.UNDECIDED)
            )
        rejected_candidates = a_models.Candidate.objects.filter(
            interviews__in = # related name of candidate in Candidate_Interview 
            a_models.Candidate_Interview.objects.filter(interview_ID=stage_id).filter(status=a_models.Candidate_Interview.REJECTED)
            )
        accepted_candidates = a_models.Candidate.objects.filter(
            interviews__in = # related name of candidate in Candidate_Interview 
            a_models.Candidate_Interview.objects.filter(interview_ID=stage_id).filter(status=a_models.Candidate_Interview.ACCEPTED)
            )
        
    else:
        raise Exception("Invalid stage type")

    return {
        'heading': job.title,
        'job': job,
        'application': stages['application'],
        'test_stages': stages['test'],
        'interview_stages': stages['interview'],
        'active_stage_name': stage_name,
        'active_stage_id': stage_id,
        'undecided_candidates': undecided_candidates,
        'accepted_candidates': accepted_candidates,
        'rejected_candidates': rejected_candidates,
    }

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def change_candidate_status(candidate_id, stage_id, stage_name, new_status):
    # TODO
    # get a standard workaround for the stage_name
    if stage_name is None or stage_id is None or candidate_id is None or (new_status not in [a_models.Candidate_Application.ACCEPTED, a_models.Candidate_Application.REJECTED, a_models.Candidate_Application.UNDECIDED]):
            raise ValueError()
    candidate = a_models.Candidate.objects.get(candidate_ID=candidate_id)
    stage = a_models.Base_Job_Stage.objects.get(id=stage_id)
    if stage_name.lower() == a_models.Application.__name__.lower(): # used this in case the name of the model changes. Not the best approach
        temp = a_models.Candidate_Application.objects.get(candidate_ID=candidate, application_ID=stage)
        temp.status = new_status
    elif stage_name.lower() == a_models.Interview.__name__.lower():
        temp = a_models.Candidate_Interview.objects.get(candidate_ID=candidate, interview_ID=stage)
        temp.status = new_status
    elif stage_name.lower() == a_models.Test.__name__.lower():
        temp = a_models.Candidate_Test.objects.get(candidate_ID=candidate, test_ID=stage)
        temp.status = new_status
    else:
        raise ValueError()
    temp.save()
    
def add_candidates_to_stage_in_bulk(stage, candidates):
    objects = []
    if isinstance(stage, a_models.Test):
        for candidate in candidates:
            objects.append(
                a_models.Candidate_Test(
                candidate_ID=candidate,
                test_ID=stage,
                status=a_models.Candidate_Test.UNDECIDED
            ))
    elif isinstance(stage, a_models.Interview):
        for candidate in candidates:
            objects.append(
                a_models.Candidate_Interview(
                candidate_ID=candidate,
                interview_ID=stage,
                status=a_models.Candidate_Interview.UNDECIDED
            ))
    else:
        raise NotImplementedError("Candidates can only be added to test and interview stages manually.")
    if len(objects) > 0:
        if isinstance(stage, a_models.Test):
            a_models.Candidate_Test.objects.bulk_create(objects)
        elif isinstance(stage, a_models.Interview):
            a_models.Candidate_Interview.objects.bulk_create(objects)
        else:
            raise NotImplementedError("Candidates can only be added to test and interview stages manually.")

def add_candidate_to_next_stage(candidate_id, current_stage_id, current_stage_name):
    """Adds the candidate to the next stage of the recruitment process if there is one.
    The candidate is created with a status of 'U' (undecided) for the next stage.

    Args:
        candidate_id (int): id of the candidate
        current_stage_id (int): id of the current stage
        current_stage_name (str): the name of the current stage (application, test, interview)

    Raises:
        ValueError: if any of the arguments are None
    """
    if candidate_id is None or current_stage_id is None or current_stage_name is None:
        raise ValueError()
    candidate = a_models.Candidate.objects.get(candidate_ID=candidate_id)
    current_stage = a_models.Base_Job_Stage.objects.get(id=current_stage_id) 
    stages = list(a_models.Base_Job_Stage.objects.filter(job_ID=current_stage.job_ID))
    current_stage_index = stages.index(current_stage)
    # there is a next stage
    if current_stage_index < len(stages) - 1:
        next_stage = stages[current_stage_index + 1]
        if isinstance(next_stage, a_models.Test):
            a_models.Candidate_Test.objects.create(
                candidate_ID=candidate,
                test_ID=next_stage,
                status=a_models.Candidate_Test.UNDECIDED
            )
        elif isinstance(next_stage, a_models.Interview):
            a_models.Candidate_Interview.objects.create(
                candidate_ID=candidate,
                interview_ID=next_stage,
                status=a_models.Candidate_Interview.UNDECIDED
            )
        print("added candidate to next stage")

def drop_candidate_from_stage(job_id, candidate_id, stage_id, stage_name):
    if stage_name is None or stage_id is None or candidate_id is None:
            raise ValueError()
    candidate = a_models.Candidate.objects.get(candidate_ID=candidate_id)
    stage = a_models.Base_Job_Stage.objects.get(id=stage_id)
    if stage_name.lower() == a_models.Application.__name__.lower():
        application = a_models.Candidate_Application.objects.get(candidate_ID=candidate, application_ID=stage)
        application.status = a_models.Candidate_Application.REJECTED
        application.save(update_fields=['status'])
    elif stage_name.lower() == a_models.Interview.__name__.lower():
        interview = a_models.Candidate_Interview.objects.get(candidate_ID=candidate, interview_ID=stage)
        interview.status = a_models.Candidate_Interview.REJECTED
        interview.save(update_fields=['status'])
    elif stage_name.lower() == a_models.Test.__name__.lower():
        test = a_models.Candidate_Test.objects.get(candidate_ID=candidate, test_ID=stage)
        test.status = a_models.Candidate_Test.REJECTED
        test.save(update_fields=['status'])
    else:
        raise ValueError()

def create_job(request):
    job_form = r_forms.JobCreationForm(request.POST)
    if job_form.is_valid():
        job = job_form.save(commit=False)
        job.created_By = request.user.recruiter
    application_form = r_forms.JobApplicationForm(request.POST)
    application = application_form.save(commit=False)
    job.save()
    application.job_ID = job
    application.created_By = request.user.recruiter
    application.save()
    

def search_candidates(request, SEARCH_TYPES):
    # TODO
    # add search by skills, experience, education, current_company
    # add ranking
    from urllib.parse import unquote
    search_term = request.GET.get('q')
    search_by = request.GET.get('type')
    search_term = unquote(search_term)
    print(search_term)
    if int(search_by) == SEARCH_TYPES['name']['value']:
        print('Hello')
        # search for first_Name + last_Name
        from django.db.models import Q
        for term in search_term.split(' '):
            candidates = a_models.Candidate.objects.filter(Q(first_Name__icontains=term) | Q(last_Name__icontains=term)).values()
    if int(search_by) == SEARCH_TYPES['skills']['value']:
        candidates = a_models.Candidate.objects.filter(candidate_application__skills__skill_Name__icontains=search_term).values()
    if int(search_by) == SEARCH_TYPES['experience']['value']:
        candidates = a_models.Candidate.objects.filter(candidate_application__experience__job_Title__icontains=search_term).values().union(
            a_models.Candidate.objects.filter(candidate_application__experience__company_Name__icontains=search_term).values()
        ) 
    if int(search_by) == SEARCH_TYPES['education']['value']:
        candidates = a_models.Candidate.objects.filter(candidate_application__education__field_Name__icontains=search_term).values().union(
            a_models.Candidate.objects.filter(candidate_application__education__institute_Name__icontains=search_term).values()
        )
    if int(search_by) == SEARCH_TYPES['job_applied']['value']:
        candidates = a_models.Candidate.objects.filter(candidate_application__application_ID__job_ID__title__icontains=search_term).values()
    print(candidates)
    return list(candidates)


def schedule_interviews():
    # TODO
    # schedule interviews for candidates
    pass


def add_approved_cand_from_prev_stage(job_id):
    stages = list(a_models.Base_Job_Stage.objects.filter(job_ID=job_id).order_by('end_Date'))
    new_stage = stages[-1]
    prev_stage = stages[-2]
    assert not_none(new_stage, prev_stage)
    if isinstance(prev_stage, a_models.Application):
        candidates = list(
            a_models.Candidate.objects.filter(
                candidate_application__application_ID=prev_stage, 
                candidate_application__status=a_models.Candidate_Application.ACCEPTED
            ))
    elif isinstance(prev_stage, a_models.Test):
        candidates = list(
            a_models.Candidate.objects.filter(
                candidate_tests__test_ID=prev_stage, 
                candidate_tests__status=a_models.Candidate_Test.ACCEPTED
            ))
    elif isinstance(prev_stage, a_models.Interview):
        candidates = a_models.Candidate.objects.filter(
            interviews__interview_ID=prev_stage, 
            interviews__status=a_models.Candidate_Interview.ACCEPTED
        )
    else:
        raise NotImplementedError("Only Application, Test and Interview stages are supported")
    add_candidates_to_stage_in_bulk(
        stage=new_stage,
        candidates=candidates
    )