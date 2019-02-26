from django.test import TestCase
from ..models import (
    Profile, 
    ProfilePhoneNumber,
    ProfileAddress,
    ProfileAttribute,
    ProfileEducation,
    ProfileLink,
    Affiliation
)
from .ischool_profiles_fixture import (
    ProfileFactory, 
    ProfilePhoneNumberFactory,
    ProfileAddressFactory,
    ProfileAttributeFactory,
    ProfileEducationFactory,
    ProfileLinkFactory,
    AffiliationFactory
)
from datetime import date, datetime, timedelta

class ProfileModelTestCase(TestCase):

    def test_age(self):
        profile = ProfileFactory.create(date_of_birth=date.today())
        profile.save()
        self.assertIsNotNone(profile.id)
        self.assertEqual(profile.get_age(), 0)

        profile.date_of_birth = date.today() - timedelta(days=400)
        profile.save()
        self.assertEqual(profile.get_age(), 1)

    def test_get_phone_numbers(self):
        profile = ProfileFactory.create()
        phone_number = ProfilePhoneNumberFactory.create(profile=profile, number='+999999999', phone_type="model type")
        phone_number.save()

        phone_number_list1 = profile.get_phone_numbers()
        phone_number_list2 = []
        for phone in ProfilePhoneNumber.objects.filter(profile=profile):
            phone_number = {'phone type' : phone.phone_type, 'best time to contact' : phone.best_contact_time,
                             'number' : phone.number}
            phone_number_list2.append(phone_number)
        self.assertEqual(phone_number_list1, phone_number_list2)

    def test_get_addresses(self):
        profile = ProfileFactory.create()
        address = ProfileAddressFactory.create(profile=profile, country="USA")
        address.save()

        addresses_list1 = profile.get_addresses()
        addresses_list2 = []
        for adr in ProfileAddress.objects.filter(profile=profile):
            address = {'street address' : adr.street_address, 'city' : adr.city,
                             'state' : adr.state, 'zip code' : adr.zip_code, 'country' : adr.country}
            addresses_list2.append(address)
        self.assertEqual(addresses_list1, addresses_list2)


    def test_get_education(self):
        profile = ProfileFactory.create()
        education = ProfileEducationFactory.create(profile=profile, degree="BS")
        education.save()
        
        education_list1 = profile.get_education()
        education_list2 = []
        for edu in ProfileEducation.objects.filter(profile=profile):
            educate = {'university' : edu.university, 'gpa' : edu.gpa, 'degree' : edu.degree, 
                        'major' : edu.major, 'location' : edu.location, 'graduation_date' : edu.graduation_date}
            education_list2.append(educate)
        self.assertEqual(education_list1, education_list2)
    
    def test_get_links(self):
        profile = ProfileFactory.create()
        link = ProfileLinkFactory.create(profile=profile, url_name="Facebook")

        link_list1 = profile.get_links()
        link_list2 = []
        for link in ProfileLink.objects.filter(profile=profile):
            linkk = {'url_name' : link.url_name , 'url_link' : link.url_link}
            link_list2.append(linkk)
        self.assertEqual(link_list1, link_list2)

    def test_get_attributes(self):
        profile = ProfileFactory.create()
        attribute = ProfileAttributeFactory.create(profile=profile, title='attribute title')
        
        attribute_list1 = profile.get_attributes()
        attribute_list2 = []
        for attr in ProfileAttribute.objects.filter(profile=profile):
            attribute = {'title' : attr.title, 'value' : attr.value , 'sort_order' : attr.sort_order}
            attribute_list2.append(attribute)
        self.assertEqual(attribute_list1, attribute_list2)
        
    def test_get_affiliations(self):
        profile = ProfileFactory.create()
        affiliation = AffiliationFactory.create(name='affiliation name')
        
        affiliation_list1 = profile.get_affiliations()
        affiliation_list2 = []
        for aff in Affiliation.objects.filter(id=profile.id):
            affiliation = {'id' : aff.id, 'name' : aff.name,
                            'academic rank' : aff.academic_rank,  
                            'AD group' : aff.associated_ad_group}
            affiliation_list2.append(affiliation)
        self.assertEqual(affiliation_list1, affiliation_list2)
        