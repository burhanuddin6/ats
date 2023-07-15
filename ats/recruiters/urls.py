from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'recruiters'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    # dashboard paths
    path('dashboard', views.dashboard, name='dashboard'),
    # candidates paths
    path('candidates', views.candidates, name='candidates'),
    # path('candidates/<int:candidate_id>', views.view_candidate, name='view_candidate'),

    # job paths
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:job_id>', views.job, name='job'),
    path('jobs/<int:job_id>/approve_candidate', views.approve_candidate, name='approve_candidate'),
    path('jobs/<int:job_id>/reject_candidate', views.reject_candidate, name='reject_candidate'),
    path('jobs/create', views.create_job, name='create_job'),

    # create job stage
    path(
        'jobs/<int:job_id>/create/stage/<str:stage_name>', 
        views.create_stage, 
        name='create_stage'
    ),
    path(
        'jobs/<int:job_id>/create/interview/<int:stage_id>/slots', 
        views.create_interview_slots, 
        name='create_interview_slots'
    ),

    ############ ajax/fetch calls ############

    # interview
    path(
        'get_div_job_candidates/<int:job_id>', 
        views.get_div_job_candidates, 
        name='get_div_job_candidates'
    ),
    path(
        'schedule_candidate_interview/<str:candidate_id>/<int:stage_id>', 
        views.schedule_candidate_interview, 
        name='schedule_candidate_interview'
    ),
    path(
        'delete_candidate_interview/<str:candidate_id>/<int:stage_id>', 
        views.delete_candidate_interview, 
        name='delete_candidate_interview'
    ),
    
    # search
    path('search', views.search_candidates, name='search_candidates'),

    # messages
    path('messages', views.get_user_messages, name='messages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
