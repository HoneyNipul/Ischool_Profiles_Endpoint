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

class TestAddressEndpoints(APITestCase):

    def setUp(self):
        self.client = APIClient()   
    
    def test_create_address(self):
        """  
        Ensure we can create a new addresss
        """  
        url = reverse('v1:addresses-list', args=[1])
        profile = ProfileFactory.create()
        
        address_data = {'profile' : str(profile.id),
                'street_address' : 'test street',
                'city' : 'test city',
                'state' : 'test state', 
                'zip_code' : 'test zip',
                'country' : 'test country',
        }

        # Check Anonymous User should return 403
        response = self.client.post(url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.post(url, address_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsNotNone(response_data["profile"])
        self.assertEqual(ProfileAddress.objects.get(profile=response_data['profile']).street_address, 'test street')
        self.assertEqual(ProfileAddress.objects.get(profile=response_data['profile']).city, address_data['city'])
        self.assertEqual(len(ProfileAddress.objects.all()), 1)
        self.assertEqual(Profile.objects.get(pk=profile.id).id, uuid.UUID(response_data['profile']))

    def test_update_address(self):
        address = ProfileAddressFactory.create()
        address_data = ProfileAddressFactory.get_update_serializer_data(address)
        address_data["profile"] = address.profile.id
        address_data["city"] = "Chicago"

        url = reverse('v1:addresses-detail', args=[1, address.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.put(url, address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIsNotNone(response_data["profile"])
        updated_address = ProfileAddress.objects.get(profile=response_data["profile"])
        self.assertEqual(updated_address.city, address_data["city"])
        self.assertEqual(len(ProfileAddress.objects.all()), 1)
    
    def test_destroy_address(self):
        """
        Ensure we can delete an address
        """
        address = ProfileAddressFactory.create(city="city_destroyed")
        
        url = reverse('v1:addresses-detail', args=[1, address.id])
        self.assertEqual(len(ProfileAddress.objects.all()), 1)

        # Check Anonymous User should return 403
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Profile Owner User
        self.client.credentials(Authorization='Bearer ' + 'regularusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(ProfileAddress.objects.all()), 0)