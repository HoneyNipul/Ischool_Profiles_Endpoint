from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import unittest
from django.test import RequestFactory
import json
from rest_framework import status   

from ischool_profiles_core.api_views import MyProfileViewSet,MyProfileHelper
from ischool_profiles_api.tests import test_profile_image_endpoints 
from ischool_profiles_core.models import (
    Profile,
    ProfileLink,
    ProfileAddress,
    ProfileAttribute,
    ProfileEducation,
    ProfilePhoneNumber,
)

from ischool_profiles_core.tests.ischool_profiles_fixture import (
    ProfileFactory,
    ProfileLinkFactory,
    ProfileAddressFactory,
    ProfileEducationFactory,
    ProfilePhoneNumberFactory,
)
from django.test import TestCase  
import unittest
from io import BytesIO
from PIL import Image
import uuid



import datetime

class MockProfileHelper(MyProfileHelper):
     def old_bio(self, userId):
        data = {
            "netId": "ndlyga",
            "lastName": "Lyga",
            "firstName": "Nicholas",
            "emailAddress": "ndlyga@syr.edu",
            "displayName": "Nick Lyga",
            "nameLastFirstInitial": "Lyga, N",
            "campusPhone": "315-443-4490",
            "campusBuilding": "Hinds Hall",
            "campusOfficeRoom": "002M",
            "photoUrl": "//my.ischool.syr.edu/Uploads/ProfilePicture/Nicholas Lyga_6617-3833-f40b8bd4-bf55-4b4a-93e9-3aa01deded59.jpg",
            "curriculumVitaePublicAccessFlag": "false",
            "curriculumVitaeUrl": "",
            "affiliations": [
                {
                "id": 5,
                "affiliationName": "Staff",
                "academicAffiliationRank": 95
                },
                {
                "id": 1,
                "affiliationName": "Adjunct Faculty",
                "academicAffiliationRank": 99
                }
            ],
            "jobTitles": [
                {
                "sortOrder": 1,
                "jobTitle": "Web Specialist II"
                },
                {
                "sortOrder": 2,
                "jobTitle": "Adjunct"
                }
            ],
            "siteLinks": [],
            "biographies": [
                {
                "bioType": "overview",
                "bioText": "<p><strong>Nick Lyga</strong> is tasked with managing the external website and many of the internal services used by our faculty and staff at the School of Information Studies at Syracuse University. He works closely with our Digital Strategy team to develop and execute recruitment and marketing initiatives for the iSchool. He also works with many of the other departments throughout the school to streamline many of the iSchool&rsquo;s internal processes.</p><p>Nick is also an adjunct professor for the School of Information Studies, where he is currently teaching IST 256: Application Programming for Information Systems. Nick brings his real life experience and knowledge of coding into the classroom. Nick has also developed educational programs and workshops for Syracuse University&rsquo;s Project Advance and Central New York Developers Meetup. Nick is also co-founder and COO of AppHammer LLC, a web and mobile application development company.</p><p>Prior to working for the School of Information Studies, Nick followed an artistic passion of his and became co-owner and lead photographer of Creative Images Photography. &nbsp;Nick also worked for Buildrr, a web development company that served clients all over the world. After making a decision to begin his own adventure, Nick created Evolution Web Solutions, web development company, that was later merged with AppHammer LLC.</p><p>Nick received his B.A. in Physics from SUNY Potsdam and is currently pursuing a master&rsquo;s degree at the School of Information Studies.</p>"
                }
            ],
            "teachingHistory": [],
            "professorOfRecord": []
        }

        convdata = self.api_to_serializer(data)
        return convdata


class TestMyProfileHelper(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.helper = MockProfileHelper()

    def test_get_or_create_profile_new(self):
        serializer = self.helper.get_or_create_profile("fakeid", "12345","nicholas","sample@syr.edu")
        self.assertIsNotNone(serializer.instance.id)

    def test_get_or_create_profile_exists(self):
        profile = ProfileFactory.create()
        serializer = self.helper.get_or_create_profile(profile.id, "12345","nicholas","sample@syr.edu")
        self.assertIsNotNone(serializer.instance.id)
    
    def test_update_my_profile(self):
        profile = ProfileFactory.create()
        profile_data = ProfileFactory.get_update_serializer_data(profile)

        profile_data["title"] = "new title"
        profile_data["biography"] = "new biography"

        url = reverse('my', args=[1])

        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unAuthorisedUser(self):
        profile = ProfileFactory.create()
        profile_data = ProfileFactory.get_update_serializer_data(profile)

        profile_data["title"] = "new title"
        profile_data["biography"] = "new biography"

        url = reverse('my', args=[1])

        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.put(url, profile_data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_get_image(self):
        from django.core.files import File

        data = {"photoUrl": "//my.ischool.syr.edu/Uploads/ProfilePicture/Nicholas Lyga_6617-3833-f40b8bd4-bf55-4b4a-93e9-3aa01deded59.jpg"}

        result = self.helper.get_image(data)
        self.assertIsNotNone(result)

        self.assertIsInstance(result, File)


    

class TestMyProfileImageUploadViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def generate_photo_file(self):
        file = BytesIO()
        profile_image = Image.new('RGBA', size=(1000, 1000), color=(255, 255, 0))
        profile_image.save(file, 'png')
        file.name = 'profileimage.png'
        file.seek(0)
        return file
    
    def test_profile_image_upload(self):
        profile = ProfileFactory.create()
        upload_url = reverse('profile-image', args=[1])
        
        # test image using bytesio
        test_image = self.generate_photo_file()

        test_image = self.generate_photo_file()
        image ={
            "profile_image": test_image
        }
        # Test anony perms
        upload_resp = self.client.post(upload_url,image, format="multipart")

        self.assertEqual(upload_resp.status_code, status.HTTP_403_FORBIDDEN)

        # Reset the file, the first attempt reads from it
        test_image = self.generate_photo_file()

        # Test admin user
        #self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        upload_resp = self.client.post(upload_url, {"profile_image": test_image }, format="multipart")
        self.assertEqual(upload_resp.status_code, status.HTTP_200_OK)

        # Test the url shows up now
        profile_updated = Profile.objects.get(pk=profile.id)
        self.assertIsNotNone(profile_updated.profile_image)




