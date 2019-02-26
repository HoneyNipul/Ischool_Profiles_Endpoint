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
    Affiliation,
)

from ischool_profiles_core.tests.ischool_profiles_fixture import (
    ProfileFactory,
    ProfileLinkFactory,
    ProfileAddressFactory,
    ProfileEducationFactory,
    ProfilePhoneNumberFactory,
    ProfileAttributeFactory
)
from django.test import TestCase  
import unittest
from io import BytesIO
from PIL import Image
import uuid

import datetime


# All API Tests should go here!
class TestAttributeEndpoints(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_attribute(self):
        """  Ensure we can create a new social link  
        """  
        url = reverse('v1:attributes-list', args=[1])
        profile = ProfileFactory.create()
        
        attribute_data = {'profile' : str(profile.id),
                'title' : 'test title', 
                'value' : 'test value',
                'sort_order': 0
        }

        # Check Anonymous User should return 403
        response = self.client.post(url, attribute_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.post(url, attribute_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsNotNone(response_data["profile"])
        self.assertEqual(ProfileAttribute.objects.get(profile=response_data['profile']).title, 'test title')
        self.assertEqual(ProfileAttribute.objects.get(profile=response_data['profile']).value, attribute_data['value'])
        self.assertEqual(len(ProfileAttribute.objects.all()), 1)
        self.assertEqual(Profile.objects.get(pk=profile.id).id, uuid.UUID(response_data['profile']))

    def test_update_attribute(self):
        """   
        Ensure we can update attribute
        """   
        attribute = ProfileAttributeFactory.create(title="original name", value="original value")
        attribute_data = ProfileAttributeFactory.get_update_serializer_data(attribute)
        attribute_data["profile"] = attribute.profile.id
        attribute_data["value"] = "changed value"

        url = reverse('v1:attributes-detail', args=[1, attribute.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, attribute_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, attribute_data, format='json')
        response_data = response.json()

        self.assertIsNotNone(response_data["profile"])
        updated_attribute = ProfileAttribute.objects.get(profile=response_data["profile"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_attribute.value, attribute_data['value'])
        self.assertEqual(len(ProfileAttribute.objects.all()), 1)
        self.assertEqual(updated_attribute.sort_order, 1)

    def test_destroy_attribute(self):
        """
        Ensure we can delete an attribute
        """
        attribute = ProfileAttributeFactory.create()
        
        url = reverse('v1:attributes-detail', args=[1, attribute.id])

        # Check Anonymous User should return 403
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(ProfileAttribute.objects.all()), 0)

    def test_list_attributes(self):
        """
        Ensure we can list the attributes in order
        """
        profile = ProfileFactory.create()
        two = ProfileAttributeFactory.create(profile=profile, title="two", sort_order=2)
        three = ProfileAttributeFactory.create(profile=profile, title="three", sort_order=3)
        one = ProfileAttributeFactory.create(profile=profile, title="one", sort_order=1)
        
        url = reverse('v1:attributes-list', args=[1])

        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.get(url, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(ProfileAttribute.objects.all()), 3)
        for attrIndx, attrVal in enumerate(response_data["results"]):
            self.assertEqual(attrIndx+1, attrVal["sort_order"])