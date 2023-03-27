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