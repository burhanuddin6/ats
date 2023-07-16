from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from applicants.models import Candidate
from applicants.helpers import generate_alphanumeric_string, create_candidate

def CandidateTestCase(TestCase):
    
    emails = ['ba09ae@gmail.com', 'aliasgherezzy@gmail.com', 'be07724@st.habib.edu.pk']
    passwords = ['testpass1', 'testpass2', 'testpass3']
    first_names = ['testfirst1', 'testfirst2', 'testfirst3']
    last_names = ['testlast1', 'testlast2', 'testlast3']
    
    def SetUp(self):
        for i in range(3):
            create_candidate(
                email=emails[i],
                password=passwords[i],
                first_Name=first_names[i],
                last_Name=last_names[i],
            )
        
    def test_create_candidates(self):
        candidates = Candidate.objects.all()
        self.assertEqual(len(candidates), 3)
        self.assertEqual(len(User.objects.all()), 3)
        for i in range(3):
            self.assertEqual(candidates[i].user.email, emails[i])
            self.assertEqual(candidates[i].user.first_name, first_names[i])
            self.assertEqual(candidates[i].user.last_name, last_names[i])
            self.assertEqual(candidates[i].user.password, passwords[i])

    def test_invalid_candidate_creation(self):
        pass
        



