from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from auth_core.api_permissions import IsOwnerOrAuthReadOnly
from .permission import IsProfileOwner
from django.core.mail import send_mail
from rest_framework.decorators import (
    api_view, 
    authentication_classes, 
    list_route, 
    detail_route,
)
import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
import json
from django.core.files import File
import io
from io import BytesIO
from io import StringIO
import base64
from PIL import Image
from ischool_profiles_core.serializers import (
    ProfilePhoneNumberSerializerV1,
    ProfileAddressSerializerV1,
    ProfileEducationSerializerV1,
    ProfileLinkSerializerV1,
    ProfileAttributeSerializerV1,
    ProfileSerializerV1,
    ProfileUpdateSerializerV1,
    ProfileImageUploadSerializerV1,
    AffiliationSerializerV1,
    ProfileSignatureV1
)
from ischool_profiles_core.models import (
    Profile, 
    ProfileAddress, 
    ProfileAttribute, 
    ProfileEducation, 
    ProfileLink,
    ProfilePhoneNumber,
    Affiliation
)
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.template.loader import get_template

# See http://www.django-rest-framework.org/

class ProfileAttributeViewSet(viewsets.ModelViewSet):
    """
    create:
    Create a new profile attributes.

    update:
    updating the existing profile attributes

    list:
    return the list of all existing profile attributes

    retrieve:
    return the given profile attributes

    partial_update:
    updating partial values of the existing profile attributes

    destroy:
    delete the profile attribute
    """
    #queryset = ProfileAttribute.objects.order_by('sort_order')
    serializer_class = ProfileAttributeSerializerV1
    permission_classes = [IsProfileOwner]
    parser_classes = (JSONParser, MultiPartParser, )

    def get_queryset(self):
        return ProfileAttribute.objects.filter(profile__owner_id=self.request.user.id).order_by('sort_order')

    def create(self, request, *args, **kwargs):
        serializer = ProfileAttributeSerializerV1(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user.id, owner_id=request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object() #getid
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user.id, owner_id=request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        
class ProfileAddressViewSet(viewsets.ModelViewSet):
    """
    A simple viewSet for viewing address of the given profile id.

    create:
    Create a new profile id's address.

    update:
    updating the existing profile id's address

    list:
    return the list of all existing profile id's address

    retrieve:
    return the given profile id's address

    partial_update:
    updating partial values of the existing profile id's address

    destroy:
    delete the profile address
    """
    queryset = ProfileAddress.objects.all()
    serializer_class = ProfileAddressSerializerV1
    permission_classes = [IsProfileOwner]
    parser_classes = (JSONParser, MultiPartParser, )

class ProfileEducationViewSet(viewsets.ModelViewSet):
    """
    A simple viewSet for viewing education of the given profile id.

    create:
    Create a new profile id's education.

    update:
    updating the existing profile id's education

    list:
    return the list of all existing profile id's education

    retrieve:
    return the given profile address

    partial_update:
    updating partial values of the existing profile id's education
    
    destroy:
    delete the profile id's education
    """
    queryset = ProfileEducation.objects.all()
    serializer_class = ProfileEducationSerializerV1
    permission_classes = [IsProfileOwner]
    parser_classes = (JSONParser, MultiPartParser, )

class ProfileLinkViewSet(viewsets.ModelViewSet):
    """
    A simple viewSet for viewing link of the given profile id.

    create:
    Create a new profile id's link.

    update:
    updating the existing profile id's link

    list:
    return the list of all existing profile id's link

    retrieve:
    return the given profile id's link

    partial_update:
    updating partial values of the existing profile id's link
    
    destroy:
    delete the profile id's link
    """
    queryset = ProfileLink.objects.all()
    serializer_class = ProfileLinkSerializerV1
    permission_classes = [IsProfileOwner]
    parser_classes = (JSONParser, MultiPartParser, )

class ProfilePhoneNumberViewSet(viewsets.ModelViewSet):
    """
    A simple viewSet for viewing phoneNumber of the given profile id.

    create:
    Create a new profile id's link.

    update:
    updating the existing profile id's link

    list:
    return the list of all existing profile id's link

    retrieve:
    return the given profile id's link

    partial_update:
    updating partial values of the existing profile id's link
    
    destroy:
    delete the profile id's link
    """
    queryset = ProfilePhoneNumber.objects.all()
    serializer_class = ProfilePhoneNumberSerializerV1
    permission_classes = [IsProfileOwner]
    parser_classes = (JSONParser, MultiPartParser, )

class AffiliationViewSet(viewsets.ModelViewSet):
    """
    A simple viewSet for viewing Afflication of the given profile id.

    create:
    Create a new profile id's affliation.

    update:
    updating the existing profile id's affliation

    list:
    return the list of all existing profile id's affliation

    retrieve:
    return the given profile id's affliation

    partial_update:
    updating partial values of the existing profile id's affliation
    
    destroy:
    delete the profile id's affliation
    """
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializerV1
    permission_classes = [IsOwnerOrAuthReadOnly]
    parser_classes = (JSONParser, MultiPartParser, )
    
class ProfileViewSet(viewsets.ModelViewSet):
    """

    create:
    Create a new profile id's view.

    update:
    updating the existing profile.

    retrieve:
    retrieve the information of the person on given id.

    update:
    updating the existing profile.

    partial_update:
    updating partial values of the existing profile. 
    
    destroy:
    delete the profile.

    upload:
    upload profilePicture for the given id. 
    
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerV1
    permission_classes = [IsOwnerOrAuthReadOnly]
    parser_classes = (JSONParser, MultiPartParser, )

    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileSerializerV1(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ProfileUpdateSerializerV1(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator_id=request.user.id, owner_id=request.user.id)
        headers = self.get_success_headers(serializer.data)
        serializer = ProfileSerializerV1(serializer.instance)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    @detail_route(methods=['post', 'put'])
    def upload(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileImageUploadSerializerV1(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfileHelper():
    """

    api_to_serializer:
    Mapping json data to fieldset.

    old_bio:
    Api call for retrieving information about particular netId holder.

    retrieve:
    retrieve the information of the person on given id.

    get_or_create_profile:
    create or fetch old profile.
    
    """
    def get_image(self,data):
        url = data["photoUrl"]
        response = requests.get('http:'+url)
        if response.ok:
            
            i = Image.open(BytesIO(response.content)) #read from the image
            file_io = BytesIO()
            i.save(file_io, format=i.format) # save it to iobytes
            file_io.name = 'profileimage.' + url.split(".")[-1]
            file_io.seek(0)
            return File(file_io) 

        return None

    def api_to_serializer(self, d):
        item = {
                "first_name": d["firstName"],
                "last_name": d["lastName"],
                "profile_type": "student",
                "gender": "na",
                "photoUrl":d["photoUrl"],
                "email_address":d["emailAddress"],
                "phone_numbers":d["campusPhone"],
                "addresses":d["campusBuilding"],
                }
        
        bioText = '';
        for bio in d["biographies"]:
                bioText = bioText + '<h2>' + bio['bioType'] + '</h2>' + bio['bioText']
                               
        item["biography"] = bioText

        afflicationsList = []
        for aff in d["affiliations"]:
            afflications ={
                "affiliationName" :aff["affiliationName"]
            }
            afflicationsList.append(afflications)
        
        item["affiliations"] = afflicationsList

        jobTittleList =[]

        for job in d["jobTitles"]:
            jobs = {
                "jobTitle" : job["jobTitle"]
            }
            jobTittleList.append(jobs)
        item["attributes"]=jobTittleList
    
        return item
                
    def old_bio(self, userId):
        response = requests.get('{}people/bio/{}?teachingHistory=true'.format(settings.ISCHOOL_API_HOST, userId), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))   
        if response.status_code == requests.codes.ok:
            data = response.json()
            
            item = self.api_to_serializer(data)
            return item
        else:
            return None

    def get_or_create_profile(self, userid, creatorid, userName, emailAddress):
        try:
            instance = Profile.objects.get(owner_id=creatorid)
            serializer = ProfileSerializerV1(instance)
            
            return serializer
           
        except Profile.DoesNotExist:
            olddata = self.old_bio(userid)
            if olddata is None:
                item = {
                "first_name": userName,
                "gender": "na",
                "email_address":emailAddress,
                }
                olddata["creator_id"] = creatorid
                olddata["owner_id"] = creatorid
                serializer = ProfileSerializerV1(data = item)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return serializer

                #return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                olddata["creator_id"] = creatorid
                olddata["owner_id"] = creatorid
               
                pserializer = ProfileSerializerV1(data = olddata)            
                pserializer.is_valid(raise_exception=True)
                pserializer.save()

                photo = self.get_image(olddata)  
                instance = pserializer.instance
                serializer = ProfileImageUploadSerializerV1(instance=instance, data= {"profile_image": photo })
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return ProfileSerializerV1(serializer.instance)


class MyProfileSignature(generics.GenericAPIView):
    """ My Profile Signature

    get:
    Generate Signature for current user.

    post:
    Email Signature of the current user their email address.
    """

    queryset = Profile.objects.order_by('sort_order')
    serializer_class = ProfileSignatureV1
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @swagger_auto_schema(operation_id="my_profile_signature", responses={200: ProfileSignatureV1(many=False)}, manual_parameters=[])
    @detail_route()
    def get(self, request, *args, **kwargs):
        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            instance = Profile.objects.get(owner_id=request.user.id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            template = get_template("emailsig.html")
            email_sig = template.render({ "profile": instance })
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
        
        data = {
            "username": request.user.username,
            "content": email_sig
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id="my_profile_signature_email")
    def post(self, request, *args, **kwargs):
        try:
            instance = Profile.objects.get(owner_id=request.user.id)
            
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        emailTo = data.get("email_to", instance.email_address)
        
        try:
            template = get_template("emailsig.html")
            email_sig = template.render({ "profile": instance })
        except:
            return Response(status.HTTP_400_BAD_REQUEST)

        try:
            send_mail('Signature', 'your email signature', 'do-not-reply@syr.edu', [emailTo], html_message=email_sig, fail_silently=False)
        except smtplib.SMTPException:
            return Response({"message": "Could not send mail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status.HTTP_200_OK)
            

class MyProfileViewSet(generics.RetrieveUpdateAPIView):
    """
    get:
    get the user information.

    put:
    update user information.
    """
    queryset = Profile.objects.order_by('sort_order')
    serializer_class = ProfileSerializerV1
    permission_classes = [IsAuthenticated]

    helper = MyProfileHelper()
    

    def get(self, request, *args, **kwargs):
        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.helper.get_or_create_profile(userId, request.user.id, request.user._name, request.user.email)
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,*args, **kwargs):

        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
        id = request.user.id
        try:
            instance = Profile.objects.get(owner_id=request.user.id)
        except Profile.DoesNotExist:
            return Response({"message": "No Profile, Get first!"}, status=status.HTTP_404_NOT_FOUND)
        #instance = self.get_object(owner_id=request.user.id)
        serializer = ProfileUpdateSerializerV1(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner_id=request.user.id)
        profile = Profile.objects.get(pk = instance.id)
        serializer = ProfileSerializerV1(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyProfileImageUploadViewSet(APIView):
        """
        post:
        upload profilePicture for the given id.
        """
        serializer_class = ProfileSerializerV1

        def post(self,request,version):
            userId = request.user.username
            if userId == '' or userId == None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            instance = Profile.objects.get(owner_id=request.user.id)
            serializer = ProfileImageUploadSerializerV1(instance=instance, data=request.data)
            if serializer.is_valid():
                newinst = serializer.save()
                serializer = ProfileSerializerV1(newinst)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
