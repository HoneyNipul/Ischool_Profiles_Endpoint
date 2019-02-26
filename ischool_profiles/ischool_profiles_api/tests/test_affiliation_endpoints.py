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
    AffiliationFactory
)
from django.test import TestCase  
import unittest
from io import BytesIO
from PIL import Image
import uuid

import datetime


# All API Tests should go here!
class TestAffiliationEndpoints(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.affiliation_data = {'name' : 'test name', 
                'academic_rank' : 1, 
                'associated_ad_group' : 'test AD group' 
        } 

    def test_create_affiliation(self): 
        """   
        Ensure we can create a new affiliation   
        """   
        url = reverse('v1:affiliations-list', args=[1]) 
 
        # Check Anonymous User should return 403 
        response = self.client.post(url, self.affiliation_data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
 
        # Admin User 
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken') 
        response = self.client.post(url, self.affiliation_data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        response_data = response.json() 
         
        self.assertIsNotNone(response_data["id"]) 
        self.assertEqual(Affiliation.objects.get(pk=response_data['id']).name, 'test name') 
        self.assertEqual(len(Affiliation.objects.all()), 1)  

    def test_udpate_affiliation(self):
        """   
        Ensure we can update affiliation   
        """   

        affiliation = AffiliationFactory.create()
        affiliation_data = AffiliationFactory.get_update_serializer_data(affiliation)
        affiliation_data["associated_ad_group"] = "test assoicated ad group"

        url = reverse('v1:affiliations-detail', args=[1, affiliation.id])

        # Check Anonymous User should return 403
        response = self.client.put(url, affiliation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.put(url, affiliation_data, format='json')
        response_data = response.json()

        self.assertIsNotNone(response_data["id"])
        updated_affiliation = Affiliation.objects.get(id=response_data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_affiliation.associated_ad_group, affiliation_data["associated_ad_group"])
        self.assertEqual(len(Affiliation.objects.all()), 1)

    def test_destroy_affiliation(self):
        """
        Ensure we can delete an affiliation
        """
        affiliation = AffiliationFactory.create()
        
        url = reverse('v1:affiliations-detail', args=[1, affiliation.id])

        # Check Anonymous User should return 403
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin User
        self.client.credentials(Authorization='Bearer ' + 'adminusertoken')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(len(Affiliation.objects.all()), 0)
