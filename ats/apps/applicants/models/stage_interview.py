import datetime
import pytz

from django.db import models
from django.utils import timezone

from .candidate import Candidate
from .recruiter import Recruiter
from .job_stages import Interview

DAYS_OF_WEEK = {
    0: 'M',
    1: 'T',
    2: 'W',
    3: 'H',
    4: 'F',
    5: 'S',
    6: 'U',
}

TIMEZONE = pytz.timezone('Asia/Karachi')


class Slot_Group(models.Model):
    """ Slot Group Model for Interviews
    Each Interview can have a slot group. Slot groups are created by recruiters 
    and are used to automate the interview slot creation process
    """
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
    def create_interview_slots(self):
        """ Creates NUMBER interview slots for the slot group
        NUMBER: NUMBERumber of slots to be created
        
        Returns a list of interview slots"""
        
        NUMBER = self.number_Of_Slots
        temp = Interview_Daily_TimeFrame.objects.filter(slot_Group_ID=self)
        print(temp)
        duration = self.interview_ID.duration
        gap = self.min_Gap_Between
        date = datetime.datetime.combine(self.start_Date, datetime.time(0, 0))
        print(date + datetime.timedelta(days=1))
        slots = []
        day_times = {}
        for obj in temp.all():
            day_times[obj.day] = obj
        # incase there was an invalid form submission
        print(temp)
        if not day_times:
            return
        while NUMBER > 0:
            day = DAYS_OF_WEEK[date.weekday()]
            if day in day_times:
                data = day_times[day]
            else:
                print(NUMBER)
                print(date)
                print(date + datetime.timedelta(days=1))
                date += datetime.timedelta(days=1)
                continue
            start = datetime.datetime.combine(date, data.start_Time)
            end = datetime.datetime.combine(date, data.end_Time)
            print(slots)
            while start + datetime.timedelta(minutes=duration) <= end:
                slots.append(
                    Interview_Slot(
                        slot_Group_ID=self,
                        datetime_Of_Interview=start.replace(tzinfo=TIMEZONE),
                    )
                )
                start += datetime.timedelta(minutes=duration + gap)
                NUMBER -= 1
                if NUMBER <= 0:
                    break
            print(NUMBER)
            print(date)
            date += datetime.timedelta(days=1)  
        Interview_Slot.objects.bulk_create(slots)

class Interview_Daily_TimeFrame(models.Model):
    slot_Group_ID = models.ForeignKey(
        to=Slot_Group,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="weekly_timeframes",
        verbose_name="Slot Group",
    )
    MONDAY = DAYS_OF_WEEK[0]
    TUESDAY = DAYS_OF_WEEK[1]
    WEDNESDAY = DAYS_OF_WEEK[2]
    THURSDAY = DAYS_OF_WEEK[3]
    FRIDAY = DAYS_OF_WEEK[4]
    SATURDAY = DAYS_OF_WEEK[5]
    SUNDAY = DAYS_OF_WEEK[6]
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
    """ Interview Slot Model for Interviews
    An interview slot contains the details of a single interview slot
    If the slot is taken, vacant is set to True
    This model is related to Candidate_Interview model through a one-to-one relationship
    TODO: Add a one-to-one relationship with Candidate_Interview model instead of foreing key
    """
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


class Candidate_Interview(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
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
        """Used in template to render a button name to schedule or reschedule interview"""
        if self.interview_Slot_ID is not None:
            return "Reschedule"
        return "Schedule"
    
    def is_interview_done(self):
        """ Check whethere the candidate's interview date has passed or not
        If candidate does not have an interview date, return False
        Else return whether the interview date has passed or not

        Returns: boolean value
        """
        if self.interview_Slot_ID is None:
            return False
        return self.interview_Slot_ID.datetime_Of_Interview < timezone.now()
    
    def is_scheduled(self):
        """ Returns false if the candidate has not been scheduled for an interview
        that is if there is no interview slot associate with the candidate"""
        return self.interview_Slot_ID is not None

    def get_interviewer(self):
        """Return interviewer name if the candidate has been scheduled for an interview
        Return empty string if the candidate has not been scheduled for an interview"""
        if self.interview_Slot_ID is None:
            return ""
        return str(self.interview_Slot_ID.slot_Group_ID.interviewer_ID)
    
    def get_interview_datetime(self):
        """Return interview datetime if the candidate has been scheduled for an interview"""
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
