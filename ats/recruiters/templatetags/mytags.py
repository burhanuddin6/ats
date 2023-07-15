from django import template
from django.conf import settings

from applicants import models as a_models

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    return field.widget.__class__.__name__

@register.simple_tag(name='in_str')
# register for strings
def in_str(input,*args):
    for arg in args:
        if arg == input:
            return "True"
    return ""

@register.simple_tag(name='sub_str')
def sub_str(input, *args):
    for arg in args:
        if input in arg.lower():
            return "True"
    print(args[0], input)
    return ""

@register.simple_tag(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key,'')

@register.simple_tag(name='get_candidate_img_src')
def get_candidate_img_src(candidate_ID):
    candidate_application = a_models.Candidate_Application.objects.get(candidate_ID=candidate_ID)
    file_name = a_models.Profile.objects.get(id=candidate_application.profile.id).photo_File_Name
    
    if file_name is None:
        file_name = ''
    path = settings.MEDIA_URL + 'candidate_documents/' + str(candidate_ID) + '/' + file_name
    print(path)
    return path

@register.simple_tag(name='get_candidate_resume_src')
def get_candidate_resume_src(candidate_ID):
    from applicants.models import Candidate
    candidate = Candidate.objects.get(candidate_ID=candidate_ID)
    file_name = candidate.candidate_application.profile.resume_File_Name
    if file_name is None:
        file_name = ''
    path = settings.MEDIA_URL + 'candidate_documents/' + str(candidate_ID) + '/' + str(file_name)
    return path

@register.simple_tag
def get_class(input_type, initial_cls=''):
    print(input_type)
    file = ['file']
    small = ["date", "number"]
    large = ["text",]
    cls = initial_cls
    if input_type in file:
        cls = 'upload'
    if input_type in small:
        cls += ' small'
    if input_type in large:
        cls += ' large'
    return cls

@register.simple_tag
def is_descriptive(input):
    true = ['reason_For_Leaving', 'job_Description']
    if input in true:
        return "True"
    return ""

@register.simple_tag
def call_method(object, method_name, *args):
    method = getattr(object, method_name)
    return method(*args)