'''
In Django Rest Framework (DRF),
an exception handler is a mechanism for handling exceptions that occur during the processing of a request. 
When an exception is raised during the processing of a request, 
DRF's exception handling system intercepts the exception and passes it to an exception handler, 
which then handles the exception and returns an appropriate response.

The exception handler is a function that takes two arguments: 
the request object and the exception object that was raised. 
The exception handler is responsible for generating an appropriate response for the given exception. 
The response can be a standard HTTP response or a custom response, depending on the requirements.

DRF provides a default exception handler that handles a number of common exceptions, 
such as NotFound, PermissionDenied, AuthenticationFailed, ValidationError, and ParseError. 
However, you can override the default exception handler by defining your own custom exception handler function.

To define a custom exception handler in DRF, 
you can use the @api_view decorator and define a function that takes two arguments: 
the request object and the exception object. 
Within the function, you can handle the exception as needed and return an appropriate response.

For example, 
here's an example of a custom exception handler that returns a custom error message when a PermissionDenied exception is raised:

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

@api_view(['GET'])
def custom_exception_handler(request, exception):
    if isinstance(exception, PermissionDenied):
        return Response({'error': 'You do not have permission to access this resource.'}, status=403)
    return Response({'error': str(exception)}, status=500)

In this example, 
the custom_exception_handler function checks if the exception is a PermissionDenied exception, 
and if so, it returns a custom error message with a 403 status code. 
If the exception is not a PermissionDenied exception, 
it returns a generic error message with a 500 status code. 
This custom exception handler can then be added to the EXCEPTION_HANDLER setting in the Django settings file.
'''

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        data = response.data
        response.data = {}
        response.data['data'] = data
        response.data['status'] = 'failure'
        response.data['status_code'] = response.status_code
        if data.get('detail'):
            response.data['message'] = data.get('detail')
        elif data.get('non_field_errors'):
            for error_msg in data.get('non_field_errors'):
                response.data['message'] = ''
                response.data['message'] += error_msg
        else:
            response.data['message'] = 'Validation Error'

    return response