from django import template
from django.conf import settings

from apps.applicants import models as a_models

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    """Returns the type of the Django form field.

    Args:
        field (object): form field object

    Returns:
        str: widget class name of the form field object
    """
    return field.widget.__class__.__name__

@register.simple_tag(name='in_str')
# register for strings
def in_str(string,*args):
    """Checks if input is equal to any of the args.

    Args:
        string (str): string to compare with args
        *args (str): an iterable of args
        arg (str): string to compare with input

    Returns:
        bool: True or False
    """
    for arg in args:
        if arg == string:
            return "True"
    return ""

@register.simple_tag(name='sub_str')
def sub_str(string, *args):
    """Checks if string is a substring of any of the args."""
    for arg in args:
        if string in arg.lower():
            return "True"
    print(args[0], string)
    return ""

@register.simple_tag(name='get_item')
def get_item(dictionary, key):
    """gets the string value of the key in the dictionary.

    Args:
        dictionary (dict): dictionary to lookup
        key (any): _description_

    Returns:
        str: value corresponding to the key in the dictionary
    """
    return dictionary.get(key,'')

@register.simple_tag(name='get_candidate_img_src')
def get_candidate_img_src(candidate_ID):
    """ gets the path of the candidate's profile picture."""
    candidate_application = a_models.Candidate_Application.objects.get(candidate_ID=candidate_ID)
    file_name = a_models.Profile.objects.get(id=candidate_application.profile.id).photo_File_Name
    
    if file_name is None:
        file_name = ''
    path = settings.MEDIA_URL + 'candidate_documents/' + str(candidate_ID) + '/' + file_name
    print(path)
    return path

@register.simple_tag(name='get_candidate_resume_src')
def get_candidate_resume_src(candidate_ID):
    """ gets the path of the candidate's resume."""
    from apps.applicants.models import Candidate #pylint: disable=import-outside-toplevel
    candidate = Candidate.objects.get(candidate_ID=candidate_ID)
    file_name = candidate.candidate_application.profile.resume_File_Name
    if file_name is None:
        file_name = ''
    path = settings.MEDIA_URL + 'candidate_documents/' + str(candidate_ID) + '/' + str(file_name)
    return path

@register.simple_tag
def get_class(input_type, initial_cls=''):
    """gets the html class selector for the input field."""
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
def is_descriptive(string):
    """ Deprecated
    Checks if the string is a descriptive field. 
    Was made to check if the string is a textarea or not.
    """
    true = ['reason_For_Leaving', 'job_Description']
    if string in true:
        return "True"
    return ""

@register.simple_tag
def call_method(obj, method_name, *args):
    """Calls the method of the object with the given method name and arguments.
    object (object): object to call the method on)
    method_name (str): name of the method to call
    *args (any): arguments to pass to the method
    """
    method = getattr(obj, method_name)
    return method(*args)
