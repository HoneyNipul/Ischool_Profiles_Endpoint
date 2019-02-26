from factory.django import DjangoModelFactory
from .. import models, serializers
from datetime import date

import factory
# see http://factoryboy.readthedocs.io/en/latest/orms.html

class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile

    first_name = "First"
    last_name = "Last"
    creator_id = "98765"
    owner_id = "98765"
    profile_type = "student"
    display_name = "Test Student"
    title = "Mr."  
    gender = "na"

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileSerializerV1(instance=obj).data

    @staticmethod
    def get_update_serializer_data(obj):
        return {'id' : obj.id,
                'first_name' : obj.first_name, 
                'last_name' : obj.last_name,
                'display_name' : obj.display_name,
                'title' : obj.title,
                'biography' : obj.biography,
                'profile_type' : obj.profile_type,
                'date_of_birth' : obj.date_of_birth,   
                'gender' : obj.gender,
                'suid' : obj.suid,
                'email_address' : obj.email_address,
                'is_private' : obj.is_private,
                'owner_id' : obj.owner_id,
                'creator_id' : obj.creator_id,
            }    

class ProfileEducationFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileEducation

    gpa = 2.55
    profile = factory.SubFactory(ProfileFactory)
    graduation_date = "2016-08-10"

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileEducationSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileEducationSerializerV1(instance=obj).data

    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile,
            'university' : obj.university, 
            'gpa' : obj.gpa,
            'degree' : obj.degree, 
            'major' : obj.major, 
            'location' : obj.location,
            'graduation_date' : obj.graduation_date
        }     
        #! there is no education, addresses, and links (Related Manager)       

class ProfileAddressFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileAddress

    profile = factory.SubFactory(ProfileFactory)
    
    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileAddressSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileAddressSerializerV1(instance=obj).data
    
    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile,
                'street_address' : obj.street_address,
                'city' : obj.city,
                'state' : obj.state, 
                'zip_code' : obj.zip_code,
                'country' : obj.country
            }    

        #! there is no education, addresses, and links (Related Manager)

class ProfileLinkFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileLink

    url_name = 'Facbeook'
    url_link = "http://www.google.com"
    profile = factory.SubFactory(ProfileFactory)

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileLinkSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileLinkSerializerV1(instance=obj).data
    
    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile, 
                'url_name' : obj.url_name,
                'url_link' : obj.url_link,
            }    

class ProfilePhoneNumberFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfilePhoneNumber
    
    number = "+999999999"
    profile = factory.SubFactory(ProfileFactory)

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfilePhoneNumberSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfilePhoneNumberSerializerV1(instance=obj).data

    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile,
            'number' : obj.number, 
            'phone_type' : obj.phone_type, 
            'best_contact_time' : obj.best_contact_time
        }
class AffiliationFactory(DjangoModelFactory):
    class Meta:
        model = models.Affiliation

    name = "test affiliation name"
    
    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.AffiliationSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.AffiliationSerializerV1(instance=obj).data

    @staticmethod
    def get_update_serializer_data(obj):
        return {'id': obj.id,
            'name' : obj.name,
            'academic_rank' : obj.academic_rank,
            'associated_ad_group' : obj.associated_ad_group
        }


class ProfileLinkFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileLink

    url_name = 'Facbeook'
    url_link = "http://www.google.com"
    profile = factory.SubFactory(ProfileFactory)

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileLinkSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileLinkSerializerV1(instance=obj).data
    
    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile, 
                'url_name' : obj.url_name,
                'url_link' : obj.url_link,
            }    

class ProfileAttributeFactory(DjangoModelFactory):
    class Meta:
        model = models.ProfileAttribute

    profile = factory.SubFactory(ProfileFactory)

    @classmethod
    def serialized(cls, *args, **kwargs):
        obj = cls.build(*args, **kwargs)
        return serializers.ProfileAttributeSerializerV1(instance=obj).data

    @staticmethod
    def serialize_from_obj(obj):
        return serializers.ProfileAttributeSerializerV1(instance=obj).data

    @staticmethod
    def get_update_serializer_data(obj):
        return {'profile' : obj.profile, 
            'title' : obj.title, 
            'value' : obj.value,
            'sort_order' : obj.sort_order,
        }