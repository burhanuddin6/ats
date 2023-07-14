from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User 
from . import email
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

def is_recruiter(user_id):
    user = User.objects.get(pk=user_id)
    a = user.groups.filter(name='Recruiters').exists()
    if not a:
        raise ValidationError("User is not a recruiter")
# Create your models here.


# ########################################################################################

# class Graduate_Fields(models.Model):
#     feild_Name = models.CharField(
#         verbose_name="Feild Name",
#         max_length=128,
#         db_index=False,
#         # validators=[(lambda x: len(x) <= 128), (lambda x: x.isalpha())]
#     )

# ########################################################################################

# class Skills(models.Model):
#     skill_Name = models.CharField(
#         verbose_name="Skill Name",
#         max_length=128,
#         db_index=False,
#         # validators=[(lambda x: len(x) <= 128), (lambda x: x.isalpha())]
#     )

########################################################################################

class Candidate(models.Model):
    candidate_ID = models.CharField(
        verbose_name="64-character Random ID string for Candidates",
        primary_key=True,
        max_length=64,
        db_index=False,
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        unique=True,
        verbose_name="User",
        related_name="candidate"
    )
    created_At = models.DateTimeField(
        verbose_name="Date and Time of Creation",
        auto_now=False,
        auto_now_add=True,
        db_index=False,
    )
    first_Name = models.CharField(
        max_length=64,
        # validators=[(lambda x: x.isalpha())]
    )
    last_Name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}({self.candidate_ID})"
    
    def get_interview_datetime(self, stage_id):
        return self.interviews.get(interview_ID=stage_id).get_interview_datetime()

    def get_interview_schedule_opt(self, stage_id):
        return self.interviews.get(interview_ID=stage_id).get_schedule_option()
    
    def is_scheduled(self, stage_id):
        return self.interviews.get(interview_ID=stage_id).is_scheduled()

########################################################################################

class Recruiter(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        unique=True,
        validators=[is_recruiter,],
        related_name="recruiter"
    )
    created_At = models.DateTimeField(
        verbose_name="Date and Time of Creation",
        auto_now=False,
        auto_now_add=True,
        db_index=False,
    )
    first_Name = models.CharField(
        max_length=64,
        # validators=[(lambda x: x.isalpha())]
    )
    last_Name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}({self.id})"

########################################################################################

class Job(models.Model):
    title = models.CharField(
        verbose_name="Job Title",
        max_length=128,
        db_index=False,
        # validators=[(lambda x: len(x) <= 128),],
    )
    description = models.TextField(
        verbose_name="Job Description",
        db_index=False,
        max_length=1024,
        # validators=[(lambda x: len(x) <= 1024),],
    )
    _25 = '25,000 - 50,000'
    _50 = '50,000 - 75,000'
    _75 = '75,000 - 100,000'
    _100 = '100,000 - 125,000'
    _125 = '125,000 - 150,000'
    _150 = '150,000 - 175,000'
    _175 = '175,000 - 200,000'
    _200 = '200,000 - 225,000'
    _225 = '225,000 - 250,000'
    _250 = '250,000 - 275,000'
    _275 = '275,000 - 300,000'
    _300 = '300,000 - 325,000'
    SALARY_RANGE_CHOICES = [
        (_25, '25,000 - 50,000'),
        (_50, '50,000 - 75,000'),
        (_75, '75,000 - 100,000'),
        (_100, '100,000 - 125,000'),
        (_125, '125,000 - 150,000'),
        (_150, '150,000 - 175,000'),
        (_175, '175,000 - 200,000'),
        (_200, '200,000 - 225,000'),
        (_225, '225,000 - 250,000'),
        (_250, '250,000 - 275,000'),
        (_275, '275,000 - 300,000'),
        (_300, '300,000 - 325,000')     
    ]
    salary_Range = models.CharField(
        verbose_name="Salary Range",
        max_length=20,
        db_index=False,
        choices=SALARY_RANGE_CHOICES,
    )
    REMOTE = 'R'
    IN_OFFICE = 'O'
    HYBRID = 'H'
    WORK_SITE_CHOICES = [
        (REMOTE, 'Remote'),
        (IN_OFFICE, 'In Office'),
        (HYBRID, 'Hybrid'),
    ]
    work_Site = models.CharField(
        verbose_name="Work Site",
        max_length=1,
        choices=WORK_SITE_CHOICES,
        db_index=False,
    )
    FULL_TIME = 'F'
    PART_TIME = 'P'
    INTERNSHIP = 'I'
    CONTRACT = 'C'
    WORK_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (INTERNSHIP, 'Internship'),
        (CONTRACT, 'Contract'),
    ]
    work_Type = models.CharField(
        verbose_name="Work Type",
        max_length=1,
        choices=WORK_TYPE_CHOICES,
        db_index=False,
    )
    STATUS_CHOICES = [
        (True, 'Open'),
        (False, 'Closed'),
    ]
    open = models.BooleanField(
        verbose_name="Job Status",
        db_index=False,
        choices=STATUS_CHOICES,
        default=True,
    )
    created_By = models.ForeignKey(
        to=Recruiter,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="jobs_created"
    )
    def __str__(self):
        return f"{self.title}({self.id})"
########################################################################################


class Profile(models.Model):
    national_ID = models.CharField(
        verbose_name="National ID Card Number",
        max_length=13,
        db_index=True,
    )
    phone = models.CharField(
        verbose_name="Phone Number",
        max_length=11,
        db_index=True,
        # validators=[(lambda x: len(x) == 11), (lambda x: x.isdigit())]
    )
    date_Of_Birth = models.DateField(
        verbose_name="Date of Birth",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
        # validators=[(lambda x: (x - datetime.date.today()).days/365 >= 18),]
    )
    photo_File_Name = models.CharField(
        max_length=64,
        null=True,
        db_index=False
    )
    resume_File_Name = models.CharField(
        max_length=64,
        db_index=False,
        null=False,
    )

##########################################################################################

class Education(models.Model):
    BACHELORS = 'B'
    MASTERS = 'M'
    PHD = 'P'
    EDUCATION_LEVEL_CHOICES = [
        (BACHELORS, 'Bachelors'),
        (MASTERS, 'Masters'),
        (PHD, 'PhD'),
    ]
    ed_Level = models.CharField(
        verbose_name="Education Level",
        max_length=1,
        db_index=False,
        choices=EDUCATION_LEVEL_CHOICES,
    )
    field_Name = models.CharField(
        verbose_name="Field of Education",
        max_length=128,
        db_index=False,
    )
    institute_Name = models.CharField(
        verbose_name="Institute Name",
        max_length=128,
        db_index=False,
        # validators=[(lambda x: len(x) <= 128),]
    )
    graduation_Year = models.IntegerField(
        verbose_name="Graduation Year",
        db_index=False,
        # validators=[(lambda x: x >= 1950), (lambda x: x <= datetime.date.today().year),],
    )

#########################################################################p###############

class Skill(models.Model):
    skill_Name = models.CharField(
        verbose_name="Skill Name",
        max_length=128,
        db_index=False,
    )
    certificate_File_Name = models.CharField(
        verbose_name="File name for certificate related to the skill",
        max_length=64,
        null=True,
        db_index=False
    )
    

########################################################################################


### Candidate Previous Job Experience - Can be blank or single entry ###

class Experience(models.Model):
    company_Name = models.CharField(
        verbose_name="Company Name",
        max_length=128,
        db_index=False,
    )
    job_Title = models.CharField(
        verbose_name="Job Title",
        max_length=128,
        db_index=False,
    )
    start_Date = models.DateField(
        verbose_name="Start Date",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
        # validators=[(lambda x: x <= datetime.date.today()),],
    )
    end_Date = models.DateField(
        verbose_name="End Date",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
        # validators=[(lambda x: x <= datetime.date.today()),],
    )
    job_Description = models.TextField(
        verbose_name="Job Description",
        db_index=False,
        max_length=1024,
    )
    salary = models.IntegerField(
        verbose_name="Salary In PKR",
        db_index=False,
        # validators=[(lambda x: x >= 25000),],
    )
    reason_For_Leaving = models.TextField(
        verbose_name="Reason For Leaving",
        db_index=False,
        max_length=1024,
    )
    job_Slip_File_Name = models.CharField(
        verbose_name="File name for job slip",
        null=True,
        max_length=64,
        db_index=False,
    )

from django.core.validators import URLValidator

class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            # Validate as if it were https:// because these are known websites
            value = 'https://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)

class Platform(models.Model):
    name = models.CharField(
        verbose_name="Platform Name",
        max_length=128,
        db_index=False,
    )
    URL = models.CharField(
        verbose_name="Platform URL",
        max_length=128,
        db_index=False,
        validators=[OptionalSchemeURLValidator()],
    )
    def __str__(self):
        return f"{self.name.capitalize()}"

class Reference(models.Model):
    # queryset choices for name
    platform_ID = models.ForeignKey(
        to=Platform,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="profiles",
    )
    profile_URL = models.CharField(
        verbose_name="LinkedIn Profile URL",
        max_length=128,
        db_index=False,
        validators=[OptionalSchemeURLValidator()]
    )


    
    
from polymorphic.models import PolymorphicModel
class Base_Job_Stage(PolymorphicModel):
    name = models.CharField(
        verbose_name="Job Stage Name",
        max_length=128,
        db_index=False,
        default="Application",
    )
    job_ID = models.ForeignKey(
        to=Job,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="job_stages"
    )
    created_By = models.ForeignKey(
        to=Recruiter,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="job_stages_created"
    )
    description = models.TextField(
        verbose_name="Description",
        db_index=False,
        max_length=1024,
        null=True,
        blank=True,
    )
    start_Date = models.DateField(
        verbose_name="Start Date",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
    )
    end_Date = models.DateField(
        verbose_name="End Date",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
    )
    
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.start_Date > self.end_Date:
            raise ValidationError("Start date cannot be greater than end date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.end_Date > datetime.date.today()
    @property
    def is_current(self):
        return self.start_Date <= datetime.date.today() <= self.end_Date
    @property
    def is_future(self):
        return self.start_Date > datetime.date.today()
    
class Application(Base_Job_Stage):
    class Meta:
        ordering = ['job_ID','start_Date', 'end_Date']
        verbose_name = "Application Stage For Jobs"
        verbose_name_plural = "Application Stages For Jobs"

class Interview(Base_Job_Stage):
    ONLINE = 'O'
    IN_PERSON = 'I'
    INTERVIEW_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (IN_PERSON, 'In Person'),
    ]
    type = models.CharField(
        verbose_name="Interview Type",
        max_length=1,
        choices=INTERVIEW_TYPE_CHOICES,
        default=ONLINE,
    )
    duration = models.IntegerField(
        verbose_name="Each Interview Duration in Minutes",
        db_index=False,
    )
    class Meta:
        ordering = ['job_ID','start_Date', 'end_Date']
        verbose_name = "Interview Stage For Jobs"
        verbose_name_plural = "Interview Stages For Jobs"

    def create_interview_slots(self, N):
        temp = Interview_Daily_TimeFrame.objects.filter(interview_ID=self.id)
        timeframes = {
            'monday': temp.get(day='M', interview_ID=self.id),
            'tuesday': temp.get(day='T', interview_ID=self.id),
            'wednesday': temp.get(day='W', interview_ID=self.id),
            'thursday': temp.get(day='H', interview_ID=self.id),
            'friday': temp.get(day='F', interview_ID=self.id),
            'saturday': temp.get(day='S', interview_ID=self.id),
            'sunday': temp.get(day='U', interview_ID=self.id)
        }
        duration = self.duration
        gap = self.min_Gap_Between
        date = self.start_Date
        slots = []
        while N > 0:
            for day in timeframes:
                start = timeframes[day].start_Time
                end = timeframes[day].end_Time
                while start + datetime.timedelta(minutes=duration) <= end:
                    slots.append({'start': start, 'end': start + datetime.timedelta(minutes=duration), 'date': date, 'day': day})
                    start += datetime.timedelta(minutes=duration + gap)
                    N -= 1
                    if N <= 0:
                        break
                date += datetime.timedelta(days=1)  
        return slots

class Slot_Group(models.Model):
    interviewer_ID = models.ForeignKey(
        to=Recruiter,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_interviews",
        verbose_name="Interviewer",
    )
    interview_ID = models.ForeignKey(
        to=Interview,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="slot_groups",
        verbose_name="Interview",
    )
    start_Date = models.DateField(
        verbose_name="Start Date",
        db_index=False,
    )
    number_Of_Slots = models.IntegerField(
        verbose_name="Number of slots",
        db_index=False,
    )
    min_Gap_Between = models.IntegerField(
        verbose_name="Gap Between Interviews in Minutes",
        db_index=False,
        default= 10,
    )

class Interview_Daily_TimeFrame(models.Model):
    slot_Group_ID = models.ForeignKey(
        to=Slot_Group,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="weekly_timeframes",
        verbose_name="Slot Group",
    )
    MONDAY = 'M'
    TUESDAY = 'T'
    WEDNESDAY = 'W'
    THURSDAY = 'H'
    FRIDAY = 'F'
    SATURDAY = 'S'
    SUNDAY = 'U'
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]
    day = models.CharField(
        verbose_name="Day",
        max_length=1,
        choices=DAY_CHOICES,
        db_index=False,
    )
    start_Time = models.TimeField(
        verbose_name="Start Time",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
    )
    end_Time = models.TimeField(
        verbose_name="End Time",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
    )    

class Interview_Slot(models.Model):
    slot_Group_ID = models.ForeignKey(
        to=Slot_Group,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="slots",
        verbose_name="Group of the slot",
    )
    datetime_Of_Interview = models.DateTimeField(
        verbose_name="Date and Time of Interview",
        auto_now=False,
        auto_now_add=False,
        db_index=False,
    )
    cancelled = models.BooleanField(
        verbose_name="Cancelation status",
        default=False,
        db_index=False,
    )
    vacant = models.BooleanField(
        verbose_name="Vacancy",
        default=True,
        db_index=False,
    )

class Test(Base_Job_Stage):
    duration = models.IntegerField(
        verbose_name="Test Duration in Minutes",
        db_index=False,
    )
    class Meta:
        ordering = ['job_ID','start_Date', 'end_Date']
        verbose_name = "Test Stage For Jobs"
        verbose_name_plural = "Test Stages For Jobs"
    
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.start_Date > self.end_Date:
            raise ValidationError("Start date cannot be greater than end date")
        stages = list(self.job_ID.job_stages.all())
        for stage in stages:
            if (not stage.pk == self.pk) and (stage.end_Date > self.start_Date or stage.end_Date > self.end_Date):
                raise ValidationError("Stage (Application, Test(s), Interview(s)) dates cannot overlap")


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Candidate_Application(models.Model):
    application_ID = models.ForeignKey(
        to=Application,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_applications"
    )
    candidate_ID = models.OneToOneField(
        to=Candidate,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_application"
    )
    ACCEPTED = 'A'
    REJECTED = 'R'
    UNDECIDED = 'U'
    STATUS_CHOICES = [
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (UNDECIDED, 'Undecided'),
    ]
    status = models.CharField(
        verbose_name="Application Status",
        max_length=1,
        choices=STATUS_CHOICES,
        db_index=False,
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        db_index=False,
        related_name="candidate_application"
    )
    education = models.ForeignKey(
        to=Education,
        on_delete=models.CASCADE,
        db_index=False,
        related_name="candidate_application"
    )
    experience = models.ForeignKey(
        to=Experience,
        on_delete=models.CASCADE,
        db_index=False,
        related_name="candidate_application"
    )
    reference = models.ForeignKey(
        to=Reference,
        on_delete=models.CASCADE,
        db_index=False,
        related_name="candidate_application"
    )
    skills = models.ManyToManyField(
        to=Skill,
        db_index=False,
        related_name="candidate_application",

    )
    def __str__(self):
        return f"(Application:{self.application_ID}, Candidate:{self.candidate_ID})"

class Candidate_Test(models.Model):
    test_ID = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_tests"
    )
    candidate_ID = models.ForeignKey(
        to=Candidate,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_tests"
    )
    ACCEPTED = 'A'
    REJECTED = 'R'
    UNDECIDED = 'U'
    STATUS_CHOICES = [
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (UNDECIDED, 'Undecided'),
    ]
    status = models.CharField(
        verbose_name="Test Status",
        max_length=1,
        choices=STATUS_CHOICES,
        db_index=False,
    )
    def __str__(self):
        return f"(Test:{self.test_Process_ID} ---for--> Candidate: {str(self.candidate_ID)})"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify_candidate()

    def notify_candidate(self):
        salutation = "Dear " + self.candidate_ID.first_Name + ","
        message, subject = '', ''
        if self.status != self.__original_status:
            if self.status == self.ACCEPTED:
                message = f"Congratulations! You have passed the test {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.title}." +\
                f"Please stay tuned for the next steps.\n" +\
                f"We wish you all the best for the remaining steps.\n"
            elif self.status == self.REJECTED:
                message = f"We are sorry to tell you that you did not pass {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.job_Name}." +\
                    "We hope that this was a good evaluative experience for you. We wish you all the best for your future endeavors.\n" +\
                    "Please feel free to apply for other jobs on our portal."
            subject = f"Test Result: {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.job_Name}"
        else:
            subject = "Test for the job {self.test_Process_ID.job_ID.job_Name}"
            message = "You need to take the test for the job application: {self.test_Process_ID.job_ID.job_Name}.\n" +\
                f"Test Name: {self.test_Process_ID.test_Name}\n" +\
                f"Test Description: {self.test_Process_ID.test_Description}\n" +\
                f"Test Duration: {self.test_Process_ID.test_Duration} minutes\n" +\
                f"Test Start Date: {self.test_Process_ID.test_Start_Date}\n" +\
                f"Test End Date: {self.test_Process_ID.test_End_Date}\n" +\
                "Please make sure that you take the test on time. The test can be taken only once.\n" +\
                "We wish you all the best for the test.\n"
        ending = "\nRegards,\n JBS Recruitment Team" +\
            "\n\nThis is an auto-generated email. Please do not reply to this email." +\
            "\nFor any queries, please contact {self.test_Process_ID.job_ID.recruiter_ID.email_ID}"
        message = salutation + "\n\n" + message + ending
        if subject:
            email.send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.candidate_ID.user.email],
                fail_silently=False,
            )


class Candidate_Interview(models.Model):
    interview_ID = models.ForeignKey(
        to=Interview,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="candidate_interviews"
    )
    candidate_ID = models.ForeignKey(
        to=Candidate,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="interviews"
    )
    ACCEPTED = 'A'
    REJECTED = 'R'
    UNDECIDED = 'U'
    STATUS_CHOICES = [
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (UNDECIDED, 'Undecided'),
    ]
    status = models.CharField(
        verbose_name="Interview Status",
        max_length=1,
        choices=STATUS_CHOICES,
        db_index=False,
    )
    interview_Slot_ID = models.ForeignKey(
        to=Interview_Slot,
        on_delete=models.SET_NULL,
        db_index=True,
        related_name="candidate_interviews",
        null=True,
        blank=True
    )
    interviewer_Remarks = models.TextField(
        verbose_name="Interviewer Remarks",
        db_index=False,
        max_length=1024,
        null=True,
        blank=True
    )
    
    # def __init__(self, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.__original_status = self.status
    #     # self.interview does not exist yet. Only self.interview_id exists at this point in init.
    #     self.__original_details = {}
    
    def get_schedule_option(self):
        if self.interview_Slot_ID is not None:
            return "Reschedule"
        return "Schedule"
    
    def is_interview_done(self):
        if self.interview_Slot_ID is None:
            return False
        return self.interview_Slot_ID.datetime_Of_Interview < timezone.now()
    
    def is_scheduled(self):
        return self.interview_Slot_ID is not None

    def get_interviewer(self):
        if self.interview_Slot_ID is None:
            return ""
        return str(self.interview_Slot_ID.slot_Group_ID.interviewer_ID)
    
    def get_interview_datetime(self):
        if self.interview_Slot_ID is None:
            return "Not Scheduled"
        return str(self.interview_Slot_ID.datetime_Of_Interview)
        

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.notify_candidate()

    # def notify_candidate(self):
    #     if self.status != self.__original_status:
    #         if self.status == "P":
    #             subject = "Interview Result"
    #             message = "Congratulations! You have passed the interview."
    #         elif self.status == "F":
    #             subject = "Interview Result"
    #             message = "Sorry, you have failed the interview."
    #         else:
    #             return
    #         email_from = settings.EMAIL_HOST_USER
    #         recipient_list = [self.candidate_ID.user.email, ]
    #         email.send_mail(subject, message, email_from, recipient_list)
    #         self.__original_status = self.status
    #     elif self.interview_details_changed(self.__original_details):
    #         if self.interview_Process_ID.interview_Type == "O":
    #             subject = "Online Interview Rescheduled"
    #             message = "You have been Rescheduled for an online interview.\nDate: " + str(self.datetime_Of_Interview.date()) + "\nTime: " + str(self.datetime_Of_Interview.time()) + "\nInterviewer: " + str(self.interviewer.first_Name) + " " + str(self.interviewer.last_Name) + "\nMeeting link: https://meet.google.com/baj-xwhy-jry\nPassword: 123456"
    #         else:
    #             subject = "In Person Interview Rescheduled"
    #             message = "You have been Rescheduled for an inperson interview.\nDate: " + str(self.datetime_Of_Interview.date()) + "\nTime: " + str(self.datetime_Of_Interview.time()) + "\nInterviewer: " + str(self.interviewer.first_Name) + " " + str(self.interviewer.last_Name) + "\nAddress: 123, ABC Street, XYZ City, 123456"
    #         message += "This is an auto-generated email. Please do not reply to this email. \nIf you have any queries, please contact " + str((self.interviewer.user).email) + "."
    #         email.send_email(
    #             subject=subject,
    #             message=message,
    #             from_email=settings.EMAIL_HOST_USER,
    #             to_email=[self.candidate_ID.user.email,],
    #             fail_silently=False,
    #         )
    #         self.__original_details = new_details
    #     else:
    #         if self.interview_Process_ID.interview_Type == "O":
    #             subject = "Online Interview Scheduled"
    #             message = "You have been scheduled for an online interview.\nDate: " + str(self.datetime_Of_Interview.date()) + "\nTime: " + str(self.datetime_Of_Interview.time()) + "\nInterviewer: " + str(self.interviewer.first_Name) + " " + str(self.interviewer.last_Name) + "\nMeeting link: https://meet.google.com/baj-xwhy-jry\nPassword: 123456"
    #         else:
    #             subject = "In Person Interview Scheduled"
    #             message = "You have been scheduled for an inperson interview.\nDate: " + str(self.datetime_Of_Interview.date()) + "\nTime: " + str(self.datetime_Of_Interview.time()) + "\nInterviewer: " + str(self.interviewer.first_Name) + " " + str(self.interviewer.last_Name) + "\nAddress: 123, ABC Street, XYZ City, 123456"
    #         message += "This is an auto-generated email. Please do not reply to this email. \nIf you have any queries, please contact " + str((self.interviewer.user).email) + "."
    #         email.send_email(
    #             subject=subject,
    #             message=message,
    #             from_email=settings.EMAIL_HOST_USER,
    #             to_email=[self.candidate_ID.user.email,],
    #             fail_silently=False,
    #         )

