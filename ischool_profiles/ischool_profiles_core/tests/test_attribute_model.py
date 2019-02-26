from django.test import TestCase
from ..models import ProfileAttribute
from .ischool_profiles_fixture import ProfileAttributeFactory, ProfileFactory

class ProfileAttributeModelTestCase(TestCase):

    def test_attribute_sort_order(self):
    
        profile = ProfileFactory.create()
        two = ProfileAttributeFactory.create(profile=profile, title="two", sort_order=2)
        three = ProfileAttributeFactory.create(profile=profile, title="three", sort_order=3)
        one = ProfileAttributeFactory.create(profile=profile, title="one", sort_order=1)
        one.save()
        two.save()
        three.save()

        for attrIndx, attrVal in enumerate(ProfileAttribute.objects.order_by('sort_order')):
            self.assertEqual(attrIndx+1,attrVal.sort_order)

    def test_attribute_update_sort_order(self):

        profile = ProfileFactory.create()

        one = ProfileAttributeFactory.create(profile=profile, title="one-one")
        two = ProfileAttributeFactory.create(profile=profile, title="two-three")
        three = ProfileAttributeFactory.create(profile=profile, title="three-two")
        one.save()
        two.save()
        three.save()

        three_data = ProfileAttributeFactory.get_update_serializer_data(three)
        three_data['sort_order'] = 2
        three.save()
        
        for attrIndx, attrVal in enumerate(ProfileAttribute.objects.order_by('sort_order')):
            print(attrVal.sort_order)
            #self.assertEqual(attrIndx+1,attrVal.sort_order)
      


