"""ischool_profiles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ischool_profiles_core import views, api_views
from rest_framework import routers, permissions
from django.http import HttpResponse, HttpResponseRedirect

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="iSchool Profiles",
      default_version='v1',
      description="iSchool Profiles API, View profiles, update your profile",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ndlyga@syr.edu"),
      license=openapi.License(name="MIT License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = routers.SimpleRouter()
# register router routes here!
router.register(r'profiles', api_views.ProfileViewSet, base_name='profiles')
router.register(r'affiliations', api_views.AffiliationViewSet, base_name='affiliations')
router.register(r'education', api_views.ProfileEducationViewSet, base_name='education')
router.register(r'links', api_views.ProfileLinkViewSet, base_name='links')
router.register(r'addresses', api_views.ProfileAddressViewSet, base_name='addresses')
router.register(r'attributes', api_views.ProfileAttributeViewSet, base_name='attributes')
router.register(r'phone_numbers', api_views.ProfilePhoneNumberViewSet, base_name='phone-numbers')

urlpatterns = [
    url(r'^api/v(?P<version>[0-9]+)/ischool-profiles/schema', schema_view.with_ui('redoc', cache_timeout=None), name='api_schema'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-profiles/my/image/', api_views.MyProfileImageUploadViewSet.as_view(), name='profile-image'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-profiles/my/signature/', api_views.MyProfileSignature.as_view(), name='profile-signature'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-profiles/my/', api_views.MyProfileViewSet.as_view(), name='my'),
    url(r'^api/v(?P<version>[0-9]+)/ischool-profiles/', include((router.urls, 'ischool_profiles_api'), namespace='v1')),
    url(r'^healthcheck/$', lambda request: HttpResponse("Healthcheck Successful", status=200)),
    url(r'', lambda request: HttpResponseRedirect("/api/v1/ischool-profiles/schema", status=301)),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
