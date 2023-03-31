# from rest_framework import serializers
# from django.contrib.auth.models import User

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')

#     def create(self, validate_data):
#         user = User.objects.create(
#             username=validate_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         return user