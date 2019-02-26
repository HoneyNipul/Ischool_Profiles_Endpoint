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

class TestLinkEndpoints(APITestCase):

    def setUp(self):
        self.client = APIClient()    
    
    def test_create_link(self):
        """  Ensure we can create a new social link  
        """  
        url = reverse('v1:links-list', args=[1])
        profile = ProfileFactory.create()
        
        link_data = {'profile' : str(profile.id),
                'url_name' : 'Facebook',
                'url_link' : 'http://www.facebook.com',
        }

        # Check Anonymous User should return 403
        response = self.client.post(url, link_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.post(url, link_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsNotNone(response_data["profile"])
        self.assertEqual(ProfileLink.objects.get(profile=response_data['profile']).url_name, 'Facebook')
        self.assertEqual(ProfileLink.objects.get(profile=response_data['profile']).url_link, link_data['url_link'])
        self.assertEqual(len(ProfileLink.objects.all()), 1)
        self.assertEqual(Profile.objects.get(pk=profile.id).id, uuid.UUID(response_data['profile']))
        
    def test_update_link(self):
        link = ProfileLinkFactory.create()
        link_data = ProfileLinkFactory.get_update_serializer_data(link)
        link_data["profile"] = link.profile.id
        link_data["url_name"] = "Google"

        url = reverse('v1:links-detail', args=[1, link.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, link_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, link_data, format='json')
        response_data = response.json()
        self.assertIsNotNone(response_data["profile"])
        updated_link = ProfileLink.objects.get(profile=response_data["profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_link.url_name, link_data["url_name"])
        self.assertEqual(len(ProfileLink.objects.all()), 1)

        #Profile.objects.get(pk=link.profile.id).links ===> comes out None. is this okay?

    def test_destroy_link(self):
        link = ProfileLinkFactory.create(url_name="link_destroy")
        url = reverse('v1:links-detail', args=[1, link.id])
    
        self.assertEqual(len(ProfileLink.objects.all()), 1)
   
        # Check Anonymous User should return 403
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(ProfileLink.objects.all()), 0)
        