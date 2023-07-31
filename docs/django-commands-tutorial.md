https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/
Note: There can be some grammatical mistakes in the commands given below. The easiest way is to Google.
Note: '...' are abbreviation for your current path
Note: These commands are mostly linux based, and I have put some windows commands too where I think is they differ

===================================================================================================================================							
Step 1: Python installation
install python and make sure python is correctly installed by typing this command in CMD or bash
... $python --version
-----------------------------------------------------------------------------------------------------------------------------------
Step 2 (optional) : Install virtual environment. You can search more about virtual environment online
... $pip install virtualenv

to create a virtual environment of your project:
... $mkdir myproj # create a project dir where the virtual environment will exist
.../myproj $virtualenv venv -p python3 # this will create a venv folder in myproj folder
.../myproj $source venv/bin/activate # will activate the virtual environment

to deactivate virtual environment (like when you are out of myproj dir)
(venv) ... $deactivate 
Note: notice the (venv) here. this shows up whenever your virtual envronment has been succesfully activated
Note: virtualenvironment may be deactivated if you close the terminal. Therefore, it is necessary to reactivate it by using the same command.
===================================================================================================================================							
Step 3: Install django
(venv) .../myproj $pip install django
Note: if you have installed virtualenv then django will only be installed for your current project
-----------------------------------------------------------------------------------------------------------------------------------
Step 4: Start the django project
(venv) .../myproj $django-admin startproject myproj
Note: this should create a directory myproject which should contain: manage.py, myproj/
File tree: myproj/---[venv/, myproj/---[manage.py, myproj/---[__init__.py, settings.py, urls.py, wsgi.py, asgi.py]]]
-----------------------------------------------------------------------------------------------------------------------------------
Step 5: Make an app (Although you can use myproj/ app, but it is the best practice not to use myproj/ directly, instead build another apps so that it is easier to scale your project)
(venv) .../myproj/myproj $ python3 manage.py startapp my_app # Linux
(venv) .../myproj/myproj $ py manage.py startapp my_app # Windows (I think python/python3 can also work, atleast one of these 3)

File tree: myproj/---[
venv/, 
myproj/---[
manage.py, 
myproj/---[__init__.py, settings.py, urls.py, wsgi.py, asgi.py],
my_app/---[admin.py, apps.py, models.py, tests.py, views.py, __init__.py, migrations/]
]
]

Note: You can find the purpose of these files in any well documented tutorial
-----------------------------------------------------------------------------------------------------------------------------------							
Step 6: Register your app (my_app) in settings.py
In settings.py go to INSTALLED APPS list and add your app. In my_app/apps.py there will be a class, whose name should be used here

settings.py
 |INSTALLED_APPS += [
 |	'my_app.apps.My_appConfig'
 |]
===================================================================================================================================							
Step 7: Specifying the database sqlite3 (it should be done automatically, but just make sure)

settings.py
 |DATABASES = {
 |    'default': {
 |        'ENGINE': 'django.db.backends.sqlite3',
 |        'NAME': BASE_DIR / 'db.sqlite3',
 |    }
 |}

Note: This is just for sqlite. If you are working with any other sql engine, you need to see their docs
===================================================================================================================================
Step 8 (optional): Time Zone

settings.py
 | TIME_ZONE = 'Asia/Karachi'
 
===================================================================================================================================
Step 9: Add your app to myproj/url.py. You can google this. This a very important step

myproj/urls.py
 |from django.urls import include
 |urlpatterns += [
 |	path('my_app/', include('catalog.urls'))
 |]
   
===================================================================================================================================
Step 10 (optional): Add code to automatically direct any url to root, to direct towards our app (my_app)

myproj/urls.py
 |from django.views.generic import RedirectView
 |urlpatterns += [
 |	path('', RedirectView.as_view(url='my_app', permanent=True))
 |]

===================================================================================================================================
Step 11 (optional): Add support to store static files like images, css, js in our project. I do not know its significance just yet, but it will be clear once we start css, js, and add image files to our project.

myproj/urls.py
 |from django.conf import settings
 |from django.conf.urls.static from static
 |urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
===================================================================================================================================
Steps 9-11 summary

myproj/urls.py
 |urlpatterns = [
 |    path('admin/', admin.site.urls),
 |    path('catalog/', include('catalog.urls')),
 |    path('', RedirectView.as_view(url='catalog/')),
 |] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

===================================================================================================================================
Step 12: Making a migration.
(venv) .../myproj/myproj $python3 manage.py makemigrations
-----------------------------------------------------------------------------------------------------------------------------------
Step 13: Apply migrations
(venv) .../myproj/myproj $python3 manage.py migrate
Note: You will have to run both commands in 12 and 13 when you make any changes in models
===================================================================================================================================
Step 14: Adding url contents to my_app/urls.py
Note: you will need to create a urls.py file inside of my_app/ directory (folder) and add the following
my_app/urls.py
 |from django.urls import path
 |from . import views # . means current directory
 |urlpatterns = [ path('', views.index, name='index')  #giving name to url mappings is very helpful	
===================================================================================================================================
Step 14: Running the server
(venv) .../myproj/myproj$ python manage.py runserver
===================================================================================================================================
Opening a shell in webapp
Note: I wont assume virtual environment from now on
myproj/ $ python3 manage.py shell
Note: This will allow me to write python code. I can manipulate the database with this, etc.
===================================================================================================================================
Django namespace bestpractices
Templates: in each app, add templates inside templates/<app_name> folder, namespacing to app_name will help django differentiate between templates of different apps
Views.py: addding app_name variable in views.py will make it easier to namespace the template actions like {% url app_name:view %}
==================================================================================================================================
Passing Arguments in templates actions.
To forward a request to a view that takes an argument we can use something like this

<template.html>
 | {% url '<app_name>: <view_name>' '<arg>' %} # look at the syntax on how to add multiple arguments here
 
<views.py>
 |def <view_name>(request, *args, **kwargs):
 
<app_name>/urls.py
 |urlpatterns += [
 |	path('<route>/<str:fil_name>', views.<view_name>, name="<name>")
 |]

This kind of syntax can be used to index users, files, and any sequence of objects that require different views based on the id of object

Note: This above description is not accurate becuase there can be a lot of slightly different/similar use cases that require different syntax.
=================================================================================================================================
!Submitting a form using POST:
The usual syntax when you want to submit a data in django (and others) is to differentiate between POST and GET requests,
A particular mistake that I have made is that I wanted a page to submit to itself. For I did not redirect the page to another instead I rendered the same page. What happened because of this is that django resubmitted data whenever I reloaded the page. Another thing that was happening was that even when I had an invalid form and I reloaded the page, the problem was that the browser used the last request, and cause I was not doing a get request submit, after one submit, the POST request just kept on repeating. 
Solution: Redirect to the same page, this way, instead of doing a post method again, doing redirect, my request method was GET because initial redirect or url request is always GET for a URL.