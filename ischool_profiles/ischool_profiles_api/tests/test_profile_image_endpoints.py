from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import json
from rest_framework import status   
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


# All API Tests should go here!

class TestProfileImageEndpoints(APITestCase):

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
        upload_url = reverse('v1:profiles-upload', args=[1, str(profile.id)])
        check_url = reverse('v1:profiles-detail', args=[1, str(profile.id)])
        # test image using bytesio
        test_image = self.generate_photo_file()

        # Test anony perms
        upload_resp = self.client.post(upload_url, {"profile_image": test_image }, format="multipart")

        self.assertEqual(upload_resp.status_code, status.HTTP_403_FORBIDDEN)

        # Reset the file, the first attempt reads from it
        test_image = self.generate_photo_file()

        # Test admin user
        #self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        upload_resp = self.client.post(upload_url, {"profile_image": test_image }, format="multipart")
        self.assertEqual(upload_resp.status_code, status.HTTP_204_NO_CONTENT)

        # Test the url shows up now
        profile_updated = Profile.objects.get(pk=profile.id)
        self.assertIsNotNone(profile_updated.profile_image)