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

class TestEducationEndpoints(APITestCase):

    def setUp(self):
        self.client = APIClient()   

    def test_create_education(self):
        """  
        Ensure we can create new education
        """  
        url = reverse('v1:education-list', args=[1])
        profile = ProfileFactory.create()
        
        education_data = {'profile' : str(profile.id),
                'university' : 'test uni', 
                'gpa' : 4.00,
                'degree' : 'test uni', 
                'major' : 'test uni', 
                'location' : 'test uni',
                'graduation_date' : datetime.datetime.strptime('01012019', '%d%m%Y').date()
        } 

        # Check Anonymous User should return 403
        response = self.client.post(url, education_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.post(url, education_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsNotNone(response_data["profile"])
        self.assertEqual(ProfileEducation.objects.get(profile=response_data['profile']).university, 'test uni')
        self.assertEqual(ProfileEducation.objects.get(profile=response_data['profile']).graduation_date, education_data['graduation_date'])
        self.assertEqual(len(ProfileEducation.objects.all()), 1)
        self.assertEqual(Profile.objects.get(pk=profile.id).id, uuid.UUID(response_data['profile']))

    
    def test_update_education(self):
        education = ProfileEducationFactory.create()
        education_data = ProfileEducationFactory.get_update_serializer_data(education)
        education_data["profile"] = education.profile.id
        education_data["gpa"] = 4.00

        url = reverse('v1:education-detail', args=[1, education.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, education_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, education_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIsNotNone(response_data["profile"])
        updated_education = ProfileEducation.objects.get(profile=response_data["profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_education.gpa, education_data["gpa"])
        self.assertEqual(len(ProfileEducation.objects.all()), 1)

    def test_destroy_education(self):
        """
        Ensure we can delete an education
        """
        education = ProfileEducationFactory.create(university="uni_destroyed")
        
        url = reverse('v1:education-detail', args=[1, education.id])
        self.assertEqual(len(ProfileEducation.objects.all()), 1)

        # Check Anonymous User should return 403
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(ProfileEducation.objects.all()), 0)