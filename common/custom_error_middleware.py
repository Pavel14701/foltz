from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if response.status_code >= 400:
            return self.custom_error_view(request, response.status_code)

        return response

    def custom_error_view(self, request: HttpRequest, status_code: int) -> HttpResponse:
        status_str = str(status_code)
        context = {
            'status_code': status_code,
            'digit_1': status_str[0],
            'digit_2': status_str[1],
            'digit_3': status_str[2],
            'error_message': {
                400: 'BAD REQUEST',
                401: 'UNAUTHORIZED',
                403: 'FORBIDDEN',
                404: 'NOT FOUND',
                405: 'METHOD NOT ALLOWED',
                406: 'NOT ACCEPTABLE',
                407: 'PROXY AUTHENTICATION REQUIRED',
                408: 'REQUEST TIMEOUT',
                409: 'CONFLICT',
                410: 'GONE',
                411: 'LENGTH REQUIRED',
                412: 'PRECONDITION FAILED',
                413: 'PAYLOAD TOO LARGE',
                414: 'URI TOO LONG',
                415: 'UNSUPPORTED MEDIA TYPE',
                416: 'RANGE NOT SATISFIABLE',
                417: 'EXPECTATION FAILED',
                418: 'I\'M A TEAPOT',
                421: 'MISDIRECTED REQUEST',
                422: 'UNPROCESSABLE ENTITY',
                423: 'LOCKED',
                424: 'FAILED DEPENDENCY',
                426: 'UPGRADE REQUIRED',
                428: 'PRECONDITION REQUIRED',
                429: 'TOO MANY REQUESTS',
                431: 'REQUEST HEADER FIELDS TOO LARGE',
                451: 'UNAVAILABLE FOR LEGAL REASONS',
                500: 'SERVER ERROR',
                501: 'NOT IMPLEMENTED',
                502: 'BAD GATEWAY',
                503: 'SERVICE UNAVAILABLE',
                504: 'GATEWAY TIMEOUT',
                505: 'HTTP VERSION NOT SUPPORTED',
                506: 'VARIANT ALSO NEGOTIATES',
                507: 'INSUFFICIENT STORAGE',
                508: 'LOOP DETECTED',
                510: 'NOT EXTENDED',
                511: 'NETWORK AUTHENTICATION REQUIRED'
            }.get(status_code, 'UNKNOWN'),
            'error_message_full': {
                400: 'The server cannot process the request due to incorrect syntax',
                401: 'The request requires user authentication',
                403: 'The user does not have rights to access the requested resource',
                404: 'The server cannot find the requested resource',
                405: 'The method specified in the request is not allowed for the resource',
                406: 'The server cannot provide the resource',
                407: 'Requires proxy authentication',
                408: 'The server waited too long and stopped waiting',
                409: 'Conflict in the current state of the resource',
                410: 'The resource is no longer available and its location is unknown',
                411: 'Requires Content-Length header',
                412: 'The condition specified in the request is not met',
                413: 'The request body is too large for the server to process',
                414: 'The requested URI is too long',
                415: 'Media request type is not supported by the server',
                416: 'The requested range cannot be satisfied',
                417: 'The expectation specified in the Expect header was not fulfilled',
                418: 'I am a kettle and only know how to boil water)',
                421: 'The request was sent to a server that cannot provide a response',
                422: 'The server understands the request, but cannot process it',
                423: 'Resource is blocked',
                424: 'The request could not be completed because the previous request failed',
                426: 'The protocol needs to be updated to continue processing',
                428: 'The server requires a precondition to be met',
                429: 'The client sent too many requests in a given period of time',
                431: 'Request header fields are too large',
                451: 'Access to the resource is prohibited for legal reasons',
                500: 'The server encountered an unexpected error',
                501: 'The server does not support the functionality required to process the request',
                502: 'The server acting as a gateway or proxy received an incorrect response from the upstream server',
                503: 'Server is temporarily unavailable',
                504: 'The server acting as a gateway or proxy did not wait for a response from the upstream server',
                505: 'HTTP protocol version is not supported by the server',
                506: 'Error related to content approval',
                507: 'The server cannot complete the request due to lack of space',
                508: 'The server encountered an infinite loop while processing the request',
                510: 'Additional extensions are required to process the request',
                511: 'Authentication required to access network'
            }.get(status_code, 'Unknown error')
        }
        return render(request, 'error.html', context, status=status_code)