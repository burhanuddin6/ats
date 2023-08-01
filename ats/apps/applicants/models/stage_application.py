from django.db import models
from django.core.validators import URLValidator

from .candidate import Candidate
from .job_stages import Application

class Profile(models.Model):
    """Candidate Profile is stored in this model
    Profile stores secondary data of the candidate
    Related to Candidate_Application model
    """
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
    """Candidate Education Model
    Related to Candidate_Application model
    TODO: Make this model one to many with Candidate_Application

    """
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


########################################################################################


### Candidate Previous Job Experience - Can be blank or single entry ###

class Experience(models.Model):
    """
    Candidate Previous Job Experience Model
    Related to Candidate_Application model
    TODO: Make this model many to one with Candidate_Application
    Candidate_Application can have multiple experiences
    """
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


class Candidate_Application(models.Model):
    """ Candidate Application Model for Applications"""
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
    def __str__(self):
        return f"(Application:{self.application_ID}, Candidate:{self.candidate_ID})"

#########################################################################p###############

class Skill(models.Model):
    """
    Candidate Skills Model
    Related to Candidate_Application model
    TODO: Make this model many to one with Candidate_Application
    Candidate_Application can have multiple skills
    """
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
    candidate_Application_ID = models.ForeignKey(
        to=Candidate_Application,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="skills"
    )


########################################################################################

class OptionalSchemeURLValidator(URLValidator):
    """
    URL Validator that allows URLs without a scheme
    """
    def __call__(self, value):
        if '://' not in value:
            # Validate as if it were https:// because these are known websites
            value = 'https://' + value
        super().__call__(value)

class Platform(models.Model):
    """
    Platforms defined by recruiters such as different profile websites such as LinkedIn, etc.
    Related to Reference model
    One to many relationship with Reference model

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
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
        return f"{str(self.name).capitalize()}"
    def clean_URL(self):
        if '://' not in self.URL:
            # Validate as if it were https:// because these are known websites
            self.URL = 'https://' + self.URL
        return self.URL

########################################################################################

class Reference(models.Model):
    """
    Candidate References Model
    Related to Candidate_Application model
    Candidate_Application can have multiple references
    TODO: Make this model many to one with Candidate_Application by adding a foreign key"""
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
    candidate_Application_ID = models.ForeignKey(
        to=Candidate_Application,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="references"
    )
    