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
    print(applicant_id)
    candidate = a_models.Candidate.objects.get(pk=applicant_id)
    job = a_models.Job.objects.get(pk=job_id)
    application = a_models.Application.objects.get(job_ID=job)
    candidate_application = a_models.Candidate_Application(
        candidate_ID=candidate,
        application_ID=application,
        status=a_models.Candidate_Application.UNDECIDED
    )
    print(request.POST)
    profile_form = a_forms.CandidateProfileForm(request.POST, request.FILES)
    education_form = a_forms.CandidateEducationForm(request.POST)
    experience_form = a_forms.CandidateExperienceForm(request.POST, request.FILES)
    skills_formset = a_forms.CandidateSkillsFormSet(request.POST, request.FILES, prefix='skills')
    # extract formset from request.POST
    references_formset = a_forms.CandidateReferencesFormSet(request.POST, prefix='references')
    print(references_formset)
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        a_forms.store_candidate_files(profile_form.cleaned_data.get('photo'), candidate.candidate_ID)
        a_forms.store_candidate_files(profile_form.cleaned_data.get('resume'), candidate.candidate_ID)
        profile.application_ID = application
        profile.photo_File_Name = profile_form.cleaned_data.get('photo').name
        profile.resume_File_Name = profile_form.cleaned_data.get('resume').name
        profile.save()
        candidate_application.profile = profile
    else:
        print(profile_form.errors)
        raise InvalidFormException("Invalid form")
    
    if education_form.is_valid():
        education = education_form.save(commit=False)
        education.application_ID = application
        education.save()
        candidate_application.education = education
    else:
        raise InvalidFormException("Invalid form")
    
    if experience_form.is_valid():
        experience = experience_form.save(commit=False)
        experience.application_ID = application
        a_forms.store_candidate_files(experience_form.cleaned_data.get('job_Slip'), candidate.candidate_ID)
        experience.job_Slip_File_Name = experience_form.cleaned_data.get('job_Slip').name
        experience.save()
        candidate_application.experience = experience
    else:
        raise InvalidFormException("Invalid form")
    
    skill_list = []
    if skills_formset.is_valid():
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
                skill.save()
                skill_list.append(skill)
    else:
        raise InvalidFormException("Invalid form")
    
    if references_formset.is_valid():
        references = references_formset.save(commit=False)
        for reference in references:
            reference.application_ID = application
            reference.save()
            candidate_application.reference = reference
            break
    else:
        for form in references_formset:
            print(form.as_table())
        raise InvalidFormException("Invalid form")

    candidate_application.save()
    candidate_application.skills.add(*skill_list)
    return True

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
    