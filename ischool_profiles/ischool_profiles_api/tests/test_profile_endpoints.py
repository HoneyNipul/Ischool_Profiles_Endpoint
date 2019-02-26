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

class TestProfileEndpoints(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.data = {'first_name' : 'Geri', 
                'last_name' : 'Madanguit',
                'display_name' : 'gerislayer',
                'title' : 'test title',
                'biography' : 'test bio',
                'profile_type' : 'student',
                'date_of_birth' : '2019-01-01T02:02:00Z',   
                'gender' : 'female',
                'suid' : '210328250',
                'email_address' : 'gemadang@syr.edu',
                'is_private' : False 
        }

    def test_update_profile(self):
        profile = ProfileFactory.create()
        profile_data = ProfileFactory.get_update_serializer_data(profile)

        profile_data["title"] = "new title"
        profile_data["biography"] = "new biography"

        url = reverse('v1:profiles-detail', args=[1, str(profile.id)])

        # Check Anonymous User should return 403
        response = self.client.put(url, profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.put(url, profile_data, format='json')
        response_data = response.json()
        self.assertIsNotNone(response_data["id"])
        new_profile = Profile.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_profile.title, profile_data["title"])
        self.assertEqual(new_profile.biography, profile_data["biography"])

    def test_get_profile_detail(self):
        """Test get detail endpoint
        """
        profile = ProfileFactory.create()
        check_url = reverse('v1:profiles-detail', args=[1, str(profile.id)])

        response = self.client.get(check_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(profile.title, data["title"])
    
    def test_destroy_profile(self):
        """ Test to check if profile can be deleted or not.
        """
        profile = ProfileFactory.create()
        check_url = reverse('v1:profiles-detail', args=[1, str(profile.id)])

        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.delete(check_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_eSignature(self):
        """ Test to check if signature is generated for given id.
        """
        profile = ProfileFactory()
        profile.owner_id = "12345"
        profile.save()
        address = ProfileAddressFactory()
        address.profile = profile
        address.save()
        url = reverse('profile-signature', args=[1])

        # Check Anonymous User should return 403
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_send_signature(self):
        """ Test to check if signature is emailed to given email address.
        """

        profile = ProfileFactory()
        profile.owner_id = "12345"
        profile.save()
        address = ProfileAddressFactory()
        address.profile = profile
        address.save()
        url = reverse('profile-signature', args=[1])

        attribute_data = {
                'email_to' : 'hnshah@syr.edu'           
        }

        # Check Anonymous User should return 403
        response = self.client.post(url, attribute_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
 
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.post(url, attribute_data,format='json')
        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
