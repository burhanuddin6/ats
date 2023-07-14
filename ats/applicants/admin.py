from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Reference)
admin.site.register(Application)
admin.site.register(Interview)
admin.site.register(Test)
admin.site.register(Candidate_Application)
admin.site.register(Candidate_Test)
admin.site.register(Candidate_Interview)
admin.site.register(Slot_Group)
admin.site.register(Interview_Daily_TimeFrame)
admin.site.register(Interview_Slot)
admin.site.register(Platform)

admin.site.site_header = "JBS Applicant Tracking System"
admin.site.index_title = "Admin App"