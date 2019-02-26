import requests
from auth_core.helpers.servicehelpers import get_access_token
from django.conf import settings

MEDIA_SERVICE_BIN_CREATE_URL = settings.MEDIA_SERVICE_BIN_CREATE_URL
# MEDIA_SERVICE_BIN_CREATE_URL = "http://localhost:8000/api/v1/ischool-media/service/bin"


class MediaServiceException(BaseException):
    def __init__(self, message, statuscode):
            self.message = message
            self.status_code = statuscode
            return super().__init__(message)

    def __str__(self):
            return "{}: {}".format(self.status_code, self.message)

class MediaService():

    def get_access_token(self):
        return get_access_token()
    
    def create_media_from_binary(self, bin_data):
        access_token = self.get_access_token()
        headers = {
            "Authorization": "Bearer " + access_token
        }
        response = requests.post(MEDIA_SERVICE_BIN_CREATE_URL, 
            files={'file': bin_data},
            headers=headers)
        
        if not response.ok:
            raise MediaServiceException(response.text, response.status_code)

        return response.json()
