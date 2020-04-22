from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import GroupSerializer

# Create your views here.

class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        账号密码登入
        """
        response = super().post(request, *args, **kwargs)
        response.data['token'] = 'Token '+response.data['token']
        response.set_cookie('token', response.data['token'])
        return response

class TestEndpoint(APIView):
    """
    测试Endpoint
    """
    def get(self, request):
        return Response("Good Job! It is a GET method.")
    
    def post(self, request):
        return Response("Good Job! It is a POST method.")
    
    def put(self, request):
        return Response("Good Job! It is a PUT method.")
    
    def delete(self, request):
        return Response("Good Job! It is a DELETE method.")


class Groups(APIView):
    """
    组
    """
    def get(self, request):
        """
        获取组
        """
        user =request.user
        serializer = GroupSerializer(user.groups.all(), many=True)
        res = {
            "groups": serializer.data,
            "name": user.first_name,
            "username": user.username,
        }
        return JsonResponse(res, safe=False)
