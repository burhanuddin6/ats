# pylint: disable=duplicate-code
import datetime

from django.db import models
from django.core.exceptions import ValidationError

from polymorphic.models import PolymorphicModel

from .job import Job
from .recruiter import Recruiter

class Base_Job_Stage(PolymorphicModel):
    """
    Base Job Stage Model
    Related to Job model
    Many to One Relationship with Job model
    Job Stages can have three types:
        1. Application
        2. Interview
        3. Test
    """
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

    ############ KNOWN BUG IN DJANGO POLYMORPHIC ############
    """If this is not done, the polymorphic manager will not work
    And Django will take all the child class objects as instance of a single child class
    This causes horrific error when deleting objects
    """
    non_polymorphic = models.Manager()
    class Meta:
        base_manager_name = 'non_polymorphic'
    ##########################################################

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.start_Date > self.end_Date:
            raise ValidationError("Start date cannot be greater than end date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_past(self):
        """ Returns True if the job stage is in the past """
        return self.end_Date > datetime.date.today()
    
    def is_current(self):
        """ Returns True if the job stage is in the present"""
        return self.start_Date <= datetime.date.today() <= self.end_Date
    
    def is_future(self):
        """ Returns True if the job stage is in the future"""
        return self.start_Date > datetime.date.today()


class Application(Base_Job_Stage):
    """ Application Stage Model for Jobs 
    Related to Job model by one-to-one relationship. Each job must have an application stage
    Related to Candidate_Application model by one-to-many relationship. 
    Each application stage can have multiple candidate applications"""
    class Meta:
        ordering = ['job_ID','start_Date', 'end_Date']
        verbose_name = "Application Stage For Jobs"
        verbose_name_plural = "Application Stages For Jobs"

class Interview(Base_Job_Stage):
    """ Interview Stage Model for Jobs """
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

class Test(Base_Job_Stage):
    """ Test Model for Jobs
    Test Stage for a job. A job can have zero, one or more test stages
    """
    duration = models.IntegerField(
        verbose_name="Test Duration in Minutes",
        db_index=False,
    )
    class Meta:
        ordering = ['job_ID','start_Date', 'end_Date']
        verbose_name = "Test Stage For Jobs"
        verbose_name_plural = "Test Stages For Jobs"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
