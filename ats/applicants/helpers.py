
import random
import string
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from .forms import *

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
      candidate = Candidate(
            candidate_ID=candidate_ID,
            first_Name=first_Name,
            last_Name=last_Name,
            user=user
      )
      candidate.save()

def save_application_data(request, applicant_id, job_id):
    print(applicant_id)
    candidate = Candidate.objects.get(pk=applicant_id)
    job = Job.objects.get(pk=job_id)
    application = Application.objects.get(job_ID=job)
    candidate_application = Candidate_Application(
        candidate_ID=candidate,
        application_ID=application,
        status=Candidate_Application.UNDECIDED
    )
    print(request.POST)
    profile_form = CandidateProfileForm(request.POST, request.FILES)
    education_form = CandidateEducationForm(request.POST)
    experience_form = CandidateExperienceForm(request.POST, request.FILES)
    skills_formset = CandidateSkillsFormSet(request.POST, request.FILES, prefix='skills')
    # extract formset from request.POST
    references_formset = CandidateReferencesFormSet(request.POST, prefix='references')
    print(references_formset)
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        store_candidate_files(profile_form.cleaned_data.get('photo'), candidate.candidate_ID)
        store_candidate_files(profile_form.cleaned_data.get('resume'), candidate.candidate_ID)
        profile.application_ID = application
        profile.photo_File_Name = profile_form.cleaned_data.get('photo').name
        profile.resume_File_Name = profile_form.cleaned_data.get('resume').name
        profile.save()
        candidate_application.profile = profile
    else:
        print(profile_form.errors)
        raise Exception("Invalid form")
    
    if education_form.is_valid():
        education = education_form.save(commit=False)
        education.application_ID = application
        education.save()
        candidate_application.education = education
    else:
        raise Exception("Invalid form")
    
    if experience_form.is_valid():
        experience = experience_form.save(commit=False)
        experience.application_ID = application
        store_candidate_files(experience_form.cleaned_data.get('job_Slip'), candidate.candidate_ID)
        experience.job_Slip_File_Name = experience_form.cleaned_data.get('job_Slip').name
        experience.save()
        candidate_application.experience = experience
    else:
        raise Exception("Invalid form")
    
    skill_list = []
    if skills_formset.is_valid():
        for skill_form in skills_formset:
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                check_file_name_size(
                    skill_form.cleaned_data.get('certificate'),
                    5*1024*1024,
                    rename=True,
                    rename_to=str(skill_form.prefix)
                )
                store_candidate_files(
                    skill_form.cleaned_data.get('certificate'),
                    candidate.candidate_ID,
                )
                skill.save()
                skill_list.append(skill)
    else:
        raise Exception("Invalid form")
    
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
        raise Exception("Invalid form")

    candidate_application.save()
    candidate_application.skills.add(*skill_list)
    return True

def is_candidate(user):
    if user.is_authenticated:
        if Candidate.objects.filter(user=user).exists():
            return True
    return False

def candidate_has_application(candidate):
    application = Candidate_Application.objects.filter(candidate_ID=candidate).first()
    if application is not None:
        return True
    return False


def is_recruiter(user):
    return user.groups.filter(name='Recruiters').exists()
    