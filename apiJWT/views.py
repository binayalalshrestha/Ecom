from django.http.response import (
    HttpResponse, 
    JsonResponse,
    )

from django.shortcuts import (
    render, 
    redirect
    )

from . models import(
    # Singer,
    # Song,
    League,
    Team,
    Player,
    Student
)

from apiJWT.serializers import (
    # SingerSerializer,
    # SongSerializer,
    LeagueSerializer,
    TeamSerializer,
    PlayerSerializer,
    StudentSerializer
    )

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets




# to learn serializer relation
# class SingerViewSet(viewsets.ModelViewSet):
#     queryset = Singer.objects.all()
#     serializer_class = SingerSerializer

# class SongViewSet(viewsets.ModelViewSet):
#     queryset = Song.objects.all()
#     serializer_class = SongSerializer
#     pagination_class=None






# League, Team and Player ViewSets :
class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class=None

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer





# Student ViewSets

class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)
    
    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Create'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer.errors)
    
    def destroy(self, request, pk):
        id = pk
        stu = Student.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data Deleted'})
    
    



'''
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=400)
        
        return Response(status=204)


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status='400')

        if not user.check_password(password):
            return Response({'error': 'Invalid Credentials'}, status='400')

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
'''

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


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
