from django import forms
from applicants import models as a_models

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username',
            }
        ),
        required=True,
        max_length=16,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password',
                'type': 'password',
            }
        ),
        required=True,
        max_length=16,
    )

class JobCreationForm(forms.ModelForm):
    class Meta:
        model = a_models.Job
        exclude = ['created_By', 'open']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Job Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Job Description',
            }),
            'salary_Range': forms.Select(attrs={
                'class': 'form-control',
            }),
            'work_Type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'work_Site': forms.Select(attrs={
                'class': 'form-control',
            }),
        }   

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = a_models.Application
        fields = ['start_Date', 'end_Date']
        widgets = {
            'start_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Start Date',
                'type': 'date',
            }),
            'end_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter End Date',
                'type': 'date',
            }),
        }

class JobInterviewForm(forms.ModelForm):
    class Meta:
        model = a_models.Interview
        exclude = ['job_ID', 'created_By']
        widgets = {
            'start_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Start Date',
                'type': 'date',
            }),
            'end_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter End Date',
                'type': 'date',
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Time in minutes',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Description',
            })
        }

class JobTestForm(forms.ModelForm):
    class Meta:
        model = a_models.Test
        exclude = ['job_ID', 'created_By']
        widgets = {
            'start_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Start Date',
                'type': 'date',
            }),
            'end_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter End Date',
                'type': 'date',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Description',
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Time in minutes',
            }),
        }

class InterviewSlotGroupForm(forms.ModelForm):
    duration = forms.IntegerField(required=True)
    class Meta:
        model = a_models.Slot_Group
        exclude = ['interview_ID']
        widgets = {
            'interviewer_ID': forms.Select(attrs={
                'class': 'form-control',
            }),
            'number_Of_Slots': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Number of Slots',
            }),
            'min_Gap_Between': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter time in minutes',
            }),
            'start_Date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Start Date',
                'type': 'date',
            }),
        }

class InterviewDailyTimeForm(forms.ModelForm):
    check = forms.BooleanField(required=False)
    class Meta:
        model = a_models.Interview_Daily_TimeFrame
        exclude = ['slot_Group_ID']
        widgets = {
            'day': forms.Select(attrs={
                'class': 'form-control',
            }),
            'start_Time': forms.TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Start Time',
                'type': 'time',
            }),
            'end_Time': forms.TimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter End Time',
                'type': 'time',
            }),
            'check': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
        }
        
# formset for interviewdailytimeform for each of the 7 days
# InterviewDailyTimeFormSet = forms.formset_factory(InterviewDailyTimeForm, extra=7)
# set initial data for each of the 7 days
# InterviewDailyTimeFormSet.initial = [
#     {'day': 'Monday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': True},
#     {'day': 'Tuesday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': True},
#     {'day': 'Wednesday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': True},
#     {'day': 'Thursday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': True},
#     {'day': 'Friday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': True},
#     {'day': 'Saturday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': False},
#     {'day': 'Sunday', 'start_Time': datetime.time(9, 0), 'end_Time': datetime.time(17, 0), 'check': False},
# ]


class EmailCandidateForm(forms.Form):
    subject = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
    ))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
    ))
