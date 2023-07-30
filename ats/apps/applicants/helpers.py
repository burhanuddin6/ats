import random
import string

from django.contrib.auth.models import User

from . import models as a_models
from . import forms as a_forms

class InvalidFormException(Exception):
    pass

def generate_password(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.printable
    letters = letters.replace('\t', '').replace(' ','').replace('\n','').replace('\r','')
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_alphanumeric_string(length):
    # subtracting vowels from the list of letters to avoid generating words (slangs especially)
    letters = [x for x in string.ascii_letters if x not in 'aeiouAEIOU'] + list(string.digits)
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_numeric_string(length):
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(length))



def create_candidate(email,password,first_Name,last_Name):
    user = User.objects.create_user(email, email, password)
    candidate_ID = generate_alphanumeric_string(32)
    candidate = a_models.Candidate(
        candidate_ID=candidate_ID,
        first_Name=first_Name,
        last_Name=last_Name,
        user=user
    )
    candidate.save()

def save_application_data(request, applicant_id, job_id):
    """Takes in request and processes all the forms and formsets in the application page

    Args:
        request (_type_): http POST request
        applicant_id (_type_): candidate_ID of the Candidate
        job_id (_type_): id of the Job

    Returns:
        if all forms and formsets are valid, returns True and None
        if any form or formset is invalid, returns False and a dictionary of the forms and formsets
    """

    candidate = a_models.Candidate.objects.get(pk=applicant_id)
    job = a_models.Job.objects.get(pk=job_id)
    application = a_models.Application.objects.get(job_ID=job)
    candidate_application = a_models.Candidate_Application(
        candidate_ID=candidate,
        application_ID=application,
        status=a_models.Candidate_Application.UNDECIDED
    )
    profile_form = a_forms.CandidateProfileForm(request.POST, request.FILES)
    education_form = a_forms.CandidateEducationForm(request.POST)
    experience_form = a_forms.CandidateExperienceForm(request.POST, request.FILES)
    skills_formset = a_forms.CandidateSkillsFormSet(request.POST, request.FILES, prefix='skills')
    # extract formset from request.POST
    references_formset = a_forms.CandidateReferencesFormSet(request.POST, prefix='references')
    
    if all([
        profile_form.is_valid(),
        education_form.is_valid(),
        experience_form.is_valid(),
        skills_formset.is_valid(),
        references_formset.is_valid()
    ]):
        pass
    else:
        return False, {
            'profile_form': profile_form,
            'education_form': education_form,
            'experience_form': experience_form,
            'skills_formset': skills_formset,
            'references_formset': references_formset
        }
    
    profile = profile_form.save(commit=False)
    a_forms.store_candidate_files(
        profile_form.cleaned_data.get('photo'), 
        candidate.candidate_ID)
    a_forms.store_candidate_files(
        profile_form.cleaned_data.get('resume'), 
        candidate.candidate_ID)
    profile.application_ID = application
    profile.photo_File_Name = profile_form.cleaned_data.get('photo').name
    profile.resume_File_Name = profile_form.cleaned_data.get('resume').name
    profile.save()
    candidate_application.profile = profile
    
    education = education_form.save(commit=False)
    education.application_ID = application
    education.save()
    candidate_application.education = education
    
    experience = experience_form.save(commit=False)
    experience.application_ID = application
    a_forms.store_candidate_files(
        experience_form.cleaned_data.get('job_Slip'), 
        candidate.candidate_ID)
    experience.job_Slip_File_Name = experience_form.cleaned_data.get('job_Slip').name
    experience.save()
    candidate_application.experience = experience
    
    candidate_application.save()

    for skill_form in skills_formset:
        if skill_form.is_valid():
            skill = skill_form.save(commit=False)
            a_forms.check_file_name_size(
                skill_form.cleaned_data.get('certificate'),
                5*1024*1024,
                rename=True,
                rename_to=str(skill_form.prefix)
            )
            a_forms.store_candidate_files(
                skill_form.cleaned_data.get('certificate'),
                candidate.candidate_ID,
            )
            skill.candidate_Application_ID = candidate_application
            skill.certificate_File_Name = skill_form.cleaned_data.get('certificate').name
            skill.save()

    references = references_formset.save(commit=False)
    for reference in references:
        reference.application_ID = application
        reference.candidate_Application_ID = candidate_application
        reference.save()
    
    return True, None

def is_candidate(user):
    if user.is_authenticated:
        if a_models.Candidate.objects.filter(user=user).exists():
            return True
    return False

def candidate_has_application(candidate):
    application = a_models.Candidate_Application.objects.filter(candidate_ID=candidate).first()
    if application is not None:
        return True
    return False


def is_recruiter(user):
    return user.groups.filter(name='Recruiters').exists()
    