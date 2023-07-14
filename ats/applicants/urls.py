from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'applicants'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'), # removed .html extension from first argument
    path('success.html', views.success, name='success'),
    path('verify', views.verify, name='verify'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('jobs/all', views.all_jobs_view, name='all_jobs'),
    path('jobs/<int:job_id>', views.job_view, name='job'),
    path('jobs/<int:job_id>/apply', views.apply_for_job, name='apply_for_job'),
    path('application/<slug:applicant_id>', views.application, name='application'),
    path('xyz', views.xyz, name='xyz'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)