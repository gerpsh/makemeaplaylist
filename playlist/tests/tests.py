from django.test import TestCase
from django.test import Client
from ..views import *
import os.path
import json

class BuildModelTests(TestCase):
    def test_build_model(self):
        post_data = json.loads(open(os.path.dirname(__file__) + '/../fixtures/test_post.json').read())
        c = Client()
        response = c.post('/playlist/build-model/', post_data)
        #print(str(response))
        #print response.status_code
