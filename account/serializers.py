from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group


class EnrollmentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password']
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.email = validated_data['username']
        user.is_staff = False
        user.is_active = True
        group = Group.objects.get(name='Student')
        user.groups.add(group)
        user.save()

        return user