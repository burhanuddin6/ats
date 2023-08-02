# pylint: disable=duplicate-code
from django.db import models

from ckeditor.fields import RichTextField

from .recruiter import Recruiter

class Job(models.Model):
    """Job Model for the ATS app"""
    title = models.CharField(
        verbose_name="Job Title",
        max_length=128,
        db_index=False,
        # validators=[(lambda x: len(x) <= 128),],
    )
    overview = RichTextField(
        verbose_name="Job Description",
    )
    responsibilities = RichTextField(
        verbose_name="Job Responsibilities",
    )
    qualifications = RichTextField(
        verbose_name="Job Qualifications",
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
