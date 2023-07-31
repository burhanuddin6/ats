

# Create your tests here.
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from django.test import TestCase, Client
# import QuerySet
from django.db.models.query import QuerySet

from apps.applicants import models as a_models, helpers as a_helpers, forms as a_forms
from apps.applicants.helpers import create_candidate
from apps.recruiters import forms as r_forms


class CandidateTestCase(TestCase):
    
    def setUp(self):
        self.emails = ['ba09ae@gmail.com', 'aliasgherezzy@gmail.com', 'be07724@st.habib.edu.pk']
        self.passwords = ['testpass1', 'testpass2', 'testpass3']
        self.first_names = ['testfirst1', 'testfirst2', 'testfirst3']
        self.last_names = ['testlast1', 'testlast2', 'testlast3']
        for i in range(3):
            create_candidate(
                email=self.emails[i],
                password=self.passwords[i],
                first_Name=self.first_names[i],
                last_Name=self.last_names[i],
            )
        
    def test_create_candidates(self):
        candidates = a_models.Candidate.objects.all()
        self.assertEqual(len(candidates), 3)
        self.assertEqual(len(User.objects.all()), 3)
        for i in range(3):
            self.assertEqual(candidates[i].user.email, self.emails[i])
            self.assertEqual(candidates[i].first_Name, self.first_names[i])
            self.assertEqual(candidates[i].last_Name, self.last_names[i])
            self.assertEqual(
                authenticate(username=self.emails[i], password=self.passwords[i]), 
                candidates[i].user)


class SlotGroupTestCase(TestCase):
    
    def setUp(self):
        self.jobs = []
        self.jobs.append(a_models.Job.objects.create(
            title='test title',
            overview='test overview',
            responsibilities='test responsibilities',
            qualifications='test qualifications',
            salary_Range=a_models.Job._100,
            work_Site=a_models.Job.IN_OFFICE,
            work_Type=a_models.Job.FULL_TIME,
            open=True,
            created_By=a_models.Recruiter.objects.create(
                first_Name = 'test first name',
                last_Name = 'test last name',
                user = User.objects.create_user(
                    email = "abc@gmail.com", 
                    password = "password", 
                    username = "username"
                )
            ))
        )
        
        
    def test_job(self):
        job = a_models.Job.objects.get(title='test title')
        message = "Job object was not created successfully."
        self.assertEqual(job.title, 'test title', message)
        self.assertEqual(job.overview, 'test overview', message)
        self.assertEqual(job.salary_Range, a_models.Job._100, message)
        self.assertEqual(job.work_Site, a_models.Job.IN_OFFICE, message)
        self.assertEqual(job.work_Type, a_models.Job.FULL_TIME, message)
        self.assertEqual(job.open, True, message)
        self.assertEqual(job.created_By.first_Name, 'test first name', message)
        self.assertEqual(job.created_By.last_Name, 'test last name', message)
        self.assertEqual(job.created_By.user.email, 'abc@gmail.com', message)

class StageTestCase(TestCase):
    
    def setUp(self):
        pass
        

class RecruiterSiteTestCase(TestCase):
    
    def setUp(self):
        self.recruiters_grp = Group.objects.create(name='Recruiters')
        self.recruiter = a_models.Recruiter.objects.create(
            first_Name = 'test first name',
            last_Name = 'test last name',
            user = User.objects.create_user( 
                email = "recruiter@ats.com", 
                username="username", 
                password = "password"
            )
        )
        self.recruiters_grp.user_set.add(self.recruiter.user)
    
    def test_setUp(self):
        """
        Checks if the setup was correct.
        This test is important for the other tests to run correctly. 
        The following test need the recruiter to be able to login
        Checks if the user is able to login in
        Checks if the user passes the is_recruiter test
        """
        c = Client()
        # A pretest to check that the recruiter is correctly defined in setUp
        logged_in = c.login(username=self.recruiter.user.username, password="password")
        assert logged_in, "Pretest: Recruiter should be able to login."
        user = auth.get_user(c)
        self.assertEqual(user, self.recruiter.user, "Pretest: User should be the recruiter.")
        self.assertTrue(
            a_helpers.is_recruiter(user), 
            "Pretest: Test user is in 'Recruiters' group. is_recruiter should be True"
        )

    
    def test_login(self):
        """Checks the login page of the recruiter site.
        Checks the status codes of the login page on GET and POST requests.
        Checks the context of the login page on GET requests.
        """
        c = Client()
        # Adding recruiter to recruiters group
        response = c.get('/recruiters/login')
        self.assertEqual(
            response.status_code, 
            200, 
            "GET request to /recruiters/login should return status code 200.")
        self.assertTrue(
            isinstance(response.context['login_form'], r_forms.LoginForm), 
            "login_form should be an instance of r_forms.LoginForm.")
        self.assertTemplateUsed(
            response, 
            'recruiters/login.html', 
            "recruiters/login.html should be used for rendering the login page.")
        # TODO : Add user authentication test
        response = c.post(
            '/recruiters/login', 
            {}, 
            follow = True, 
            content_type='application/x-www-form-urlencoded')
        self.assertEqual(
            response.status_code, 
            200, 
            "POST request to /recruiters/login should return status code 200.")
        # login_form = r_forms.LoginForm({'username':recruiter.user.email, 'password': 'password'})

        logged_in = c.login( #pylint: disable=unused-variable
            username = self.recruiter.user.username, 
            password = "password"
        )
        response = c.get('/recruiters/login')
        self.assertEqual(
            response.status_code, 
            302, 
            "GET request to /recruiters/login with user \
                logged in should return status code 302 due to redirection to index.")


    def test_dashboard(self):
        """
        Checks the dashboard page of the recruiter site.
        Checks if the correct template is used
        Checks the status codes of the dashboard page on GET requests
        with user logged in and logged out.
        """
        c = Client()
        response = c.get('/recruiters/dashboard')
        
        
        self.assertEqual(
            response.status_code, 
            302, 
            "GET request to /recruiters/dashboard with user \
                not logged in should return status code 302."
        )
        
        # A pretest to check that the recruiter is correctly defined in setUp
        logged_in = c.login ( #pylint: disable=unused-variable
            username = self.recruiter.user.username, 
            password = "password"
        ) 
        
        response = c.get('/recruiters/dashboard')
        self.assertTemplateUsed(response, "recruiters/dashboard.html")
        self.assertEqual(
            response.status_code, 
            200, 
            "GET request to /recruiters/dashboard with user \
                logged in should return status code 200."
        )

    def test_jobs(self):
        """
        Checks the jobs page of the recruiter site.
        Checks the status codes of the jobs page on GET requests.
        Checks the context of the jobs page on GET requests.
        """
        c = Client()
        # Adding recruiter to recruiters group
        response = c.get('/recruiters/jobs')
        self.assertEqual(
            response.status_code, 
            302, 
            "GET request to /recruiters/jobs should return status code 302.")

        # A pretest to check that the recruiter is correctly defined in setUp
        logged_in = c.login( #pylint: disable=unused-variable
            username = self.recruiter.user.username, 
            password = "password"
        )

        response = c.get('/recruiters/jobs')
        self.assertEqual(
            response.status_code, 
            200, 
            "GET request to /recruiters/jobs should return status code 200.")
        self.assertTrue(
            isinstance(response.context['jobs'], QuerySet), 
            "jobs should be an instance of QuerySet.")
        self.assertTemplateUsed(
            response, 
            'recruiters/jobs.html', 
            "recruiters/jobs.html should be used for rendering the jobs page.")
        