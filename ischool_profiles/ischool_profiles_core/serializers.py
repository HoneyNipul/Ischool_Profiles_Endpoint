from rest_framework import serializers
from ischool_profiles_core.models import Profile
from ischool_profiles_core.models import (
    ProfilePhoneNumber,
    ProfileAddress,
    ProfileAttribute,
    ProfileEducation,
    ProfileLink,
    Affiliation
)
from django.db import transaction
from .services import MediaService, MediaServiceException
import logging

logger = logging.getLogger(__name__)

class ProfileAddressSerializerV1(serializers.ModelSerializer):
    """ ProfileAddressModelSerializer
    """
    street_address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    zip_code = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ProfileAddress
        fields = ('id', 'profile', 'street_address', 'city', 'state', 'zip_code', 'country')

class ProfileAttributeSerializerV1(serializers.ModelSerializer):
    """ ProfileAttributeModelSerializer
    """
    value = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ProfileAttribute
        fields = ('id', 'profile', 'title', 'value', 'sort_order')

    def create(self, validated_data, *args, **kwargs):
        """Create and return a new Attribute along with adjusting sign order numbers, given the validated data.
        """
        profile = validated_data["profile"]
        sort_order = validated_data["sort_order"]
        new_attribute = ProfileAttribute(
            profile = profile,
            title = validated_data["title"],
            value = validated_data["value"],
            sort_order = sort_order
        )   
        new_attribute.save()

        return {'profile' : new_attribute.profile, 'title': new_attribute.title, 'value': new_attribute.value, 
                'sort_order': new_attribute.sort_order}

    def update(self, instance, validated_data):
        """Update 'ProfileAttribute' instance, given the validated data.
        """
        mod_attribute = instance
        mod_attribute.profile = validated_data.get('profile', mod_attribute.profile)
        mod_attribute.title = validated_data.get('title', mod_attribute.title)
        mod_attribute.value = validated_data.get('value', mod_attribute.value)
        mod_attribute.sort_order = validated_data.get('sort_order', mod_attribute.sort_order)
        mod_attribute.save()

        return {'profile' : mod_attribute.profile, 'title': mod_attribute.title, 'value': mod_attribute.value, 
                'sort_order': mod_attribute.sort_order}
class ProfileEducationSerializerV1(serializers.ModelSerializer):
    """ ProfileEducationModelSerializer
    """
    gpa = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)
    major = serializers.CharField(required=False, allow_blank=True)
    graduation_date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])


    class Meta:
        model = ProfileEducation
        fields = ('id', 'profile', 'university', 'gpa', 'degree', 'major', 'location', 'graduation_date')

class ProfileLinkSerializerV1(serializers.ModelSerializer):
    """ ProfileLinkSerializer
    """
    class Meta:
        model = ProfileLink
        fields = ('id', 'profile', 'url_name', 'url_link')

class ProfilePhoneNumberSerializerV1(serializers.ModelSerializer):
    """ ProfilePhoneNumberSerializer
    """
    class Meta:
        model = ProfilePhoneNumber
        fields = ('id', 'profile', 'number', 'phone_type', 'best_contact_time', 'is_primary')

class AffiliationSerializerV1(serializers.ModelSerializer):
    """ AffiliationSerializerV1
    """
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    
    class Meta:
            model = Affiliation
            fields = ('id', 'name', 'academic_rank', 'associated_ad_group')


class ProfileMediaDataSerializer(serializers.Serializer):
    hash = serializers.CharField(required=False)
    public_url = serializers.CharField(required=False)
    filename = serializers.CharField(required=False)

class ProfileSerializerV1(serializers.ModelSerializer):
    """ ProfileModelSerializer
    """
    biography = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES)
    profile_type = serializers.ChoiceField(choices=Profile.PROFILE_TYPES)
    profile_image = serializers.ImageField(read_only=True)
    media_data = ProfileMediaDataSerializer(read_only=True)
    #profile_image = serializers.ReadOnlyField()
    is_private = serializers.ReadOnlyField()

    attributes = ProfileAttributeSerializerV1(many=True, read_only=True)
    affiliations = AffiliationSerializerV1(many=True, read_only=True)
    education = ProfileEducationSerializerV1(many=True, read_only=True)
    addresses = ProfileAddressSerializerV1(many=True, read_only=True)
    links = ProfileLinkSerializerV1(many=True, read_only=True)
    phone_numbers = ProfilePhoneNumberSerializerV1(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'display_name', 'title', 'profile_image', 'media_data',
                'biography', 'profile_type', 'addresses', 'links', 'phone_numbers',
                'date_of_birth', 'gender', 'suid', 'education',
                'email_address', 'attributes', 'affiliations',
                'is_private', 'owner_id', 'creator_id')


class ProfileUpdateSerializerV1(serializers.ModelSerializer):
    """ ProfileUpdateSerializer
    """            
    biography = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES, required=False)
    profile_type = serializers.ChoiceField(choices=Profile.PROFILE_TYPES, required=False)
    profile_image = serializers.ImageField(read_only=True)
    #profile_image = serializers.ReadOnlyField()
    is_private = serializers.ReadOnlyField()
    media_data = ProfileMediaDataSerializer(read_only=True)

    attributes = ProfileAttributeSerializerV1(many=True, read_only=True)
    education = ProfileEducationSerializerV1(many=True, read_only=True)
    addresses = ProfileAddressSerializerV1(many=True, read_only=True)
    links = ProfileLinkSerializerV1(many=True, read_only=True)
    phone_numbers = ProfilePhoneNumberSerializerV1(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'display_name', 'title', 'profile_image', 'media_data',
                'biography', 'profile_type', 'addresses', 'links', 'phone_numbers',
                'date_of_birth', 'gender', 'suid', 'education',
                'email_address', 'attributes', 'is_private', 'owner_id', 'creator_id')
  
    def update(self, instance, validated_data):
        """
        Update 'Profile' instance, given the validated data.
        """

        mod_profile = instance
        mod_profile.first_name = validated_data.get('first_name', mod_profile.first_name)
        mod_profile.last_name = validated_data.get('last_name', mod_profile.last_name) 
        mod_profile.title = validated_data.get('title', mod_profile.biography)
        mod_profile.display_name = validated_data.get('display_name', mod_profile.display_name) 
        #mod_profile.profile_image = validated_data.get('profile_image', mod_profile.profile_image)
        mod_profile.biography = validated_data.get('biography', mod_profile.biography)
        mod_profile.date_of_birth = validated_data.get('date_of_birth', mod_profile.date_of_birth)
        mod_profile.suid = validated_data.get('suid', mod_profile.suid)
        mod_profile.email_address = validated_data.get('email_address', mod_profile.email_address)

        mod_profile.is_private = validated_data.get('is_private', mod_profile.is_private)

        mod_profile.profile_type = validated_data["profile_type"]
        mod_profile.gender = validated_data.get('gender', mod_profile.gender)
        
        mod_profile.save()
    
        return {'id' : mod_profile.id, 'first_name' : mod_profile.first_name, 'last_name' : mod_profile.last_name, 
                'display_name' : mod_profile.display_name, 'title' : mod_profile.title,  
                'biography' : mod_profile.biography, 'profile_type' : mod_profile.profile_type,
                'date_of_birth' : mod_profile.date_of_birth,
                'gender' : mod_profile.gender, 'suid' : mod_profile.suid, 'email_address' : mod_profile.email_address, 'is_private' : mod_profile.is_private,
                'owner_id' : mod_profile.owner_id, 'creator_id' : mod_profile.creator_id}

class ProfileImageUploadSerializerV1(serializers.Serializer):
    profile_image = serializers.ImageField(max_length=None, allow_empty_file=True)
    def validate_image(self, value):
        # @todo add validation
        return value

    def update(self, instance, validated_data):
        instance.profile_image = validated_data["profile_image"]
        mservice = MediaService()
        try:
            result = mservice.create_media_from_binary(instance.profile_image.file)
            instance.media_data = result
        except MediaServiceException as err:
            logger.error(err)
        instance.save()
        return instance


class ProfileSignatureV1(serializers.Serializer):
    username = serializers.CharField()
    content = serializers.CharField()