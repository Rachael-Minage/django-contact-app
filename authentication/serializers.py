from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib import auth


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)


    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']

    def validate(self, attrs):
        email= attrs.get('email', '')
        username = attrs.get('username', '')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain alpha numeric characters")
        
        return attrs
           

    def create(self, validated_data):
        user = User.objects.create(**validated_data)  
        user.save()

        return user

    