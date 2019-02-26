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

class TestPhoneNumberEndpoints(APITestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_phone_number(self):
        """  
        Ensure we can create new phone numbers
        """  
        url = reverse('v1:phone-numbers-list', args=[1])
        profile = ProfileFactory.create()
        
        phone_number_data = {'profile' : str(profile.id),
            'number' : "+999999999", 
            'phone_type' : "personal phone", 
            'best_contact_time' : "everyday"
        }

        # Check Anonymous User should return 403
        response = self.client.post(url, phone_number_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Regular User User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.post(url, phone_number_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsNotNone(response_data["profile"])
        self.assertEqual(ProfilePhoneNumber.objects.get(profile=response_data['profile']).number, '+999999999')
        self.assertEqual(len(ProfilePhoneNumber.objects.all()), 1)
    
    def test_update_phone_number(self):
        phone_number = ProfilePhoneNumberFactory.create()
        phone_number_data = ProfilePhoneNumberFactory.get_update_serializer_data(phone_number)
        phone_number_data["profile"] = phone_number.profile.id
        phone_number_data["phone_type"] = "mobile"

        url = reverse('v1:phone-numbers-detail', args=[1, phone_number.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, phone_number_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, phone_number_data, format='json')
        response_data = response.json()

        self.assertIsNotNone(response_data["profile"])
        updated_phone_number = ProfilePhoneNumber.objects.get(profile=response_data["profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_phone_number.phone_type, phone_number_data["phone_type"])

    def test_destroy_phone_number(self):
        """
        Ensure we can delete a phone number
        """
        phone_number = ProfilePhoneNumberFactory.create(number="+999999999")
        
        url = reverse('v1:phone-numbers-detail', args=[1, phone_number.id])

        # Check Anonymous User should return 403
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(ProfilePhoneNumber.objects.all()), 0)