from django.contrib import admin

# Register your models here.
from . import models as a_models

admin.site.register(a_models.Candidate)
admin.site.register(a_models.Recruiter)
admin.site.register(a_models.Job)
admin.site.register(a_models.Education)
admin.site.register(a_models.Skill)
admin.site.register(a_models.Experience)
admin.site.register(a_models.Profile)
admin.site.register(a_models.Reference)
admin.site.register(a_models.Application)
admin.site.register(a_models.Interview)
admin.site.register(a_models.Test)
admin.site.register(a_models.Candidate_Application)
admin.site.register(a_models.Candidate_Test)
admin.site.register(a_models.Candidate_Interview)
admin.site.register(a_models.Slot_Group)
admin.site.register(a_models.Interview_Daily_TimeFrame)
admin.site.register(a_models.Interview_Slot)
admin.site.register(a_models.Platform)

admin.site.site_header = "JBS Applicant Tracking System"
admin.site.index_title = "Admin App"
