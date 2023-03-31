from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



















'''from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')
    
class UserAPIView(RetrieveAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user'''
    

# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from .serializers import UserSerializer

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         })



# class LoginView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token)
#             })

#         return Response({"detail": "Invalid credentials."}, status=401)
