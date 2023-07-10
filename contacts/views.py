from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ContactListSerializer
from .models import Contact
from rest_framework import permissions

#Create your views here.

class ContactListAPIView(ListCreateAPIView):
    serializer_class = ContactListSerializer
    queryset = Contact.objects.all()
    


class ContactDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactListSerializer
    queryset = Contact.objects.all()
    lookup_field = "id"
