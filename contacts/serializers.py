from rest_framework import serializers
from .models import Contact


class ContactListSerializer(serializers.ModelSerializer):
    id  = serializers.IntegerField(read_only=True)


    class Meta:
        model =  Contact
        fields = ['id','name','phone_number', 'email','category','created_at']