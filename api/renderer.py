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
from rest_framework.utils.serializer_helpers import ReturnDict


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
       

        response_dict = {
            'status': True,
            'message': 'Successful',
            'data': data
        }
        response = renderer_context['response']

        if response.status_code >= 200 and response.status_code <= 299:
            response_dict['status'] = True
        else:
            response_dict['status'] = False
        
            if data and data.get('data'):
                data = data.get("data")
            try:
                errors = [data[k][0] for k in data]
                response_dict['message'] =list(data.keys())[0] + " - " + errors[0] 
            except Exception:
                response_dict['message'] = 'Unsuccessful'
        if type(data) in (ReturnDict, dict):

            if data.get('data') is not None:
                response_dict['data'] = data.get('data')
            else:
                response_dict['data'] = data

            if data.get('status') == False:
                response_dict['status'] = False

            # elif data.get('status'):
            #     response_dict['status'] = data.get('status')
            #     data.pop('status')

            # if data.get('status') in ['failure', False]:
            #
            #     if data.get('error_data'):
            #         response_dict['error_data'] = data.get('error_data')
            #     else:
            #         response_dict['error_data'] = {}
            #     if data.get('error_message'):
            #         response_dict['error_message'] = data.get('error_message')
            #     else:
            #         response_dict['error_message'] = ""

            if data.get('message'):
                response_dict['message'] = data.get('message')
                data.pop('message')
            elif data.get('detail'):
                response_dict['message'] = data.get('detail')
                data.pop('detail')

        data = response_dict
        return super().render(data, accepted_media_type, renderer_context)
    









    
# from rest_framework.renderers import JSONRenderer
# from rest_framework import renderers
# from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
# from django.core.serializers.json import DjangoJSONEncoder

# class CustomJSONRenderer(JSONRenderer):

#     def render(self, data, accepted_media_type=None, renderer_context=None):

#         response_data = {
#             'status': 'success',
#             'data': data
#         }
#         return super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)