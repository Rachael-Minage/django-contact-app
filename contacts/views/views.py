from django.shortcuts import render, get_object_or_404,redirect
from contacts.serializers import ContactListSerializer
from contacts.models.models import Contact
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from contacts.forms.forms import ContactForm, EditContactForm
from django.contrib import messages




@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of contacts",
    responses={200: openapi.Response("List of contacts", ContactListSerializer(many=True))},
)
@swagger_auto_schema(
    method='post',
    operation_description="Create a new contact",
    request_body=ContactListSerializer,
    responses={201: openapi.Response("Created contact", ContactListSerializer()), 400: "Bad request"},
)
@api_view(['GET', 'POST'])
def contact_list_view(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ContactListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




@swagger_auto_schema(
    method='GET',
    operation_description='Retrieve a contact',
    responses={
        200: ContactListSerializer,
        404: 'Contact not found'
    }
)
@swagger_auto_schema(
    method='PUT',
    operation_description='Update a contact',
    responses={
        200: ContactListSerializer,
        404: 'Contact not found'
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description='Delete a contact',
    responses={
        204: ContactListSerializer,
        404: 'Contact not found'
    }
)
@api_view(['GET', 'PUT', 'DELETE'])
def contact_detail_view(request, id):
    try:
        contact = Contact.objects.get(id=id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactListSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactListSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def index(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/index.html', {'contacts': contacts})

def addContact(request):
    return render(request, 'contacts/new.html')

def create_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact saved successfully.')
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'contacts/new.html', {'form': form})

def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        form = EditContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact-profile', id=id)
    else:
        form = EditContactForm(instance=contact)
    return render(request, 'contacts/edit.html', {'form': form, 'contact': contact})

def contact_profile(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render(request, 'contacts/contact_profile.html', {'contact': contact})

def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        contact.delete()
        return redirect('index')
    return render(request, 'contacts/delete_contact.html', {'contact': contact})



