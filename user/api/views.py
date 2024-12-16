from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from user.models import Message
from user.api.serializers import MessageSerializer
from rest_framework.pagination import PageNumberPagination  


class StandardResultsSetPagination(PageNumberPagination):  
    page_size = 100  
    page_size_query_param = 'page_size'  
    max_page_size = 1000  


class MessageListView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request: Request) -> Response:
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)