from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def is_recruiter(user_id):
    """Checks whether a the user is in the Recruiters group

    Args:
        user_id (int): the pk of the user (Django User model)

    Raises:
        ValidationError: The user is not in the Recruiters group
    """
    user = User.objects.get(pk=user_id)
    boolean = user.groups.filter(name='Recruiters').exists()
    if not boolean:
        raise ValidationError("User is not a recruiter")


class Recruiter(models.Model):
    """ Recruiter Model for the ATS app
    Different than the Recruiter Group. But Each Recruiter is a member of the Recruiter Group
    """
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