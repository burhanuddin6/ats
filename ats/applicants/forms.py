from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from . import models as a_models
#import settings

def check_file_name_size(file_obj, size_limit, rename=False, rename_to=''):
    file_name = file_obj.name.split('.')
    ext = file_name[-1]
    if file_obj.size > size_limit:
        raise ValueError("File exceeds size limit")
    if ext in settings.IMAGE_FILE_TYPES or ext in settings.DOCUMENT_FILE_TYPES:
        if rename:
            file_obj.name = rename_to + '.' + ext
            return True
    else:
        raise ValueError("File type is not supported. Supported file types are:\n" + 
                         '\n'.join([str(x) for x in (settings.IMAGE_FILE_TYPES + settings.DOCUMENT_FILE_TYPES)])
        )

def store_candidate_files(file_obj, candidate_ID):
    file_system = FileSystemStorage(
            location=settings.MEDIA_ROOT + '/candidate_documents/' + str(candidate_ID) + '/'
        )
    if file_system.exists(file_obj.name):
        file_system.delete(file_obj.name)
    file_system.save(file_obj.name, file_obj)

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'abc@xyz.com',
            }
        ),
        required=True,
        max_length=254,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter',
            }
        ),
        required=True,
        max_length=16,
    )

    
class VerifyForm(forms.Form):
    verification_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Verification Code',
            }
        ),
        required=True,
        max_length=16,
    )
    

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password',
            }
        ),
        required=True,
        max_length=16,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
            }
        ),
        required=True,
        max_length=16,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email',
            }
        ),
        required=True,
        max_length=254,
    )
    class Meta:
        model = a_models.Candidate
        exclude = ['candidate_ID','created_At', 'user']
    
    def normalize(self):
        self.cleaned_data['first_Name'] = self.cleaned_data['first_Name'].capitalize()
        self.cleaned_data['last_Name'] = self.cleaned_data['last_Name'].capitalize()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        if not (cleaned_data.get("first_Name").isalpha() and cleaned_data.get("last_Name").isalpha()):
            raise forms.ValidationError("Name can only contain alphabets")
        
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        
        self.normalize()
        return self.cleaned_data
    

class CandidateProfileForm(forms.ModelForm):
    photo = forms.ImageField(

        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Photo',
            }
        )
    )
    resume = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Resume',
            }
        ),
        required=True,
    )
    class Meta:
        model = a_models.Profile
        exclude = ['photo_File_Name', 'resume_File_Name']
        widgets = {
            'date_Of_Birth': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        check_file_name_size(photo, settings.SMALL_FILE_SIZE, rename=True, rename_to='photo')
        self.photo_File_Name = photo.name
        print('filename',self.photo_File_Name)
        print('Hello')
        return photo
    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        print('hweoeir')
        check_file_name_size(resume, settings.LARGE_FILE_SIZE, rename=True, rename_to='resume')
        self.resume_File_Name = resume.name
        print('Hello')
        return resume

class CandidateEducationForm(forms.ModelForm):
    class Meta:
        model = a_models.Education
        exclude = ['application_ID']
        widgets = {
            'ed_Level': forms.Select(attrs={'class': 'form-control'}),
            'field_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'institute_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation_Year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CandidateSkillsForm(forms.ModelForm):
    certificate = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Certification If Any',
            }
        ),
    )
    class Meta:
        model = a_models.Skill
        exclude = ['application_ID', 'certificate_File_Name']
    def clean_certificate(self):
        certificate = self.cleaned_data.get("certificate")
        check_file_name_size(certificate, settings.SMALL_FILE_SIZE, rename=True, rename_to='certificate')
        self.certificate_File_Name = certificate.name
        return certificate

CandidateSkillsFormSet = forms.modelformset_factory(
    model=a_models.Skill,
    form=CandidateSkillsForm,
    extra=1,
    can_delete=True,
    max_num=20,
)


class CandidateExperienceForm(forms.ModelForm):
    job_Slip = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Job Slip',
            }
        )
    )
    class Meta:
        model = a_models.Experience
        exclude = ['application_ID','job_Slip_File_Name']
        widgets = {
            'start_Date': forms.DateInput(attrs={'type': 'date'}),
            'end_Date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_job_Slip(self):
        job_Slip = self.cleaned_data.get("job_Slip")
        check_file_name_size(job_Slip, settings.SMALL_FILE_SIZE, rename=True, rename_to='job_Slip')
        self.job_Slip_File_Name = job_Slip.name
        return job_Slip
        

class CandidateDocumentsForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Photo',
            }
        ),
        required=True,
    )
    job_Slip = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Upload Job Slip',
            }
        ),
        required=True,
    )

    def rename(self):
        for key in self.cleaned_data:
            data = self.cleaned_data[key]
            data.name = str(key) + '.' + data.name.split('.')[1]
    
    def store(self, candidate_ID):
        file_system = FileSystemStorage(
            location=settings.MEDIA_ROOT + 'candidate_documents/' + str(candidate_ID) + '/'
        )
        for key in self.cleaned_data:
            data = self.cleaned_data[key]
            if file_system.exists(data.name):
                file_system.delete(data.name)
            file_system.save(data.name, data)

    def clean(self):
        cleaned_data = self.cleaned_data

        resume = cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Resume must be in PDF format")
            if resume.size > settings.CANDIDATE_RESUME_SIZE_LIMIT:
                raise forms.ValidationError("Resume size must be less than 10MB")
        return self.cleaned_data



class CandidateReferencesForm(forms.ModelForm):
    class Meta:
        model = a_models.Reference
        exclude = ['application_ID']
        widgets = {
            'platform_ID': forms.Select(attrs={'class': 'form-control'}),
            'profile_URL': forms.TextInput(attrs={'class': 'form-control'}),
        }

# make a formset for references
CandidateReferencesFormSet = forms.modelformset_factory(
    a_models.Reference,
    form=CandidateReferencesForm,
    extra=1,
    max_num=20,
    can_delete=True,
    widgets={
        'platform_ID': forms.Select(attrs={'class': 'form-control'}),
        'profile_URL': forms.TextInput(attrs={'class': 'form-control'}),
    },
)


####################################DEBUG#########################################################
