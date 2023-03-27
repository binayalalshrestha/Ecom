'''
A JSON renderer is a component in a web framework or API framework that converts Python objects 
into JSON (JavaScript Object Notation) strings that can be sent as responses to HTTP requests.
The JSON renderer is responsible for serializing the Python objects into a JSON format and
then sending them over the network as part of an HTTP response.

In the Django REST Framework, the JSON renderer is used to serialize the responses of API views
and render them in a JSON format. The JSON renderer takes the response data 
(which is typically a Python dictionary or list) and converts it to a JSON string 
that can be understood by the client requesting the data.

Custom JSON renderers can be created to modify the way that responses are serialized 
and structured, such as adding additional keys or modifying the structure of the response data. 
This can be useful for enforcing consistent API responses across an application or 
integrating with a specific client-side application or library.
'''
from rest_framework.renderers import JSONRenderer
from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from rest_framework.renderers import JSONRenderer
from django.core.serializers.json import DjangoJSONEncoder

class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response_data = {
            'status': 'success',
            'data': data
        }
        return super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)