# pylint: disable=duplicate-code
from django.db import models

from .candidate import Candidate
from .job_stages import Test


class Candidate_Test(models.Model):
    """ Candidate Test Model for Tests"""
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
        return f"(Test:{self.test_ID} ---for--> Candidate: {str(self.candidate_ID)})"

    # def __init__(self, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.__original_status = self.status

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.notify_candidate()

    # def notify_candidate(self):
    #     salutation = "Dear " + self.candidate_ID.first_Name + ","
    #     message, subject = '', ''
    #     if self.status != self.__original_status:
    #         if self.status == self.ACCEPTED:
    #             message = f"Congratulations! You have passed the test {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.title}." +\
    #             "Please stay tuned for the next steps.\n" +\
    #             "We wish you all the best for the remaining steps.\n"
    #         elif self.status == self.REJECTED:
    #             message = f"We are sorry to tell you that you did not pass {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.job_Name}." +\
    #                 "We hope that this was a good evaluative experience for you. We wish you all the best for your future endeavors.\n" +\
    #                 "Please feel free to apply for other jobs on our portal."
    #         subject = f"Test Result: {self.test_Process_ID.test_Name} for the job {self.test_Process_ID.job_ID.job_Name}"
    #     else:
    #         subject = "Test for the job {self.test_Process_ID.job_ID.job_Name}"
    #         message = "You need to take the test for the job application: {self.test_Process_ID.job_ID.job_Name}.\n" +\
    #             f"Test Name: {self.test_Process_ID.test_Name}\n" +\
    #             f"Test Description: {self.test_Process_ID.test_Description}\n" +\
    #             f"Test Duration: {self.test_Process_ID.test_Duration} minutes\n" +\
    #             f"Test Start Date: {self.test_Process_ID.test_Start_Date}\n" +\
    #             f"Test End Date: {self.test_Process_ID.test_End_Date}\n" +\
    #             "Please make sure that you take the test on time. The test can be taken only once.\n" +\
    #             "We wish you all the best for the test.\n"
    #     ending = "\nRegards,\n JBS Recruitment Team" +\
    #         "\n\nThis is an auto-generated email. Please do not reply to this email." +\
    #         "\nFor any queries, please contact {self.test_Process_ID.job_ID.recruiter_ID.email_ID}"
    #     message = salutation + "\n\n" + message + ending
    #     if subject:
    #         email.send_mail(
    #             subject=subject,
    #             message=message,
    #             from_email=settings.EMAIL_HOST_USER,
    #             recipient_list=[self.candidate_ID.user.email],
    #             fail_silently=False,
    #         )
