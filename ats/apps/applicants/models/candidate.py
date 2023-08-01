from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    """Candidate Model for the ATS app
    A user is a candidate only if they have an entry in this table
    A candidate also has a single candidate_application

    TODO: Add tests for this model

    Args:
        Does not have an overriden __init__ method
        Uses the default __init__ method
    
    """
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
        """_summary_

        Args:
            stage_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.interviews.get(interview_ID=stage_id).get_interview_datetime()

    def get_interview_schedule_opt(self, stage_id):
        """_summary_

        Args:
            stage_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.interviews.get(interview_ID=stage_id).get_schedule_option()
    
    def is_scheduled(self, stage_id):
        """_summary_
        """
        return self.interviews.get(interview_ID=stage_id).is_scheduled()
