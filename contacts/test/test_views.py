import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from contacts.models import Contact
from contacts.serializers import ContactListSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_contact_list_view(api_client):
    contact1 = Contact.objects.create(name='John Doe', phone_number='1234567890', email='john.doe@example.com',
                                      category='FRIEND')
    contact2 = Contact.objects.create(name='Jane Smith', phone_number='9876543210', email='jane.smith@example.com',
                                      category='WORK')

    # Send GET request to the contact_list_view
    url = reverse('contacts')
    response = api_client.get(url)

    # Check the response status code and data
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Assuming there are two contacts in the database
    serialized_data = ContactListSerializer([contact1, contact2], many=True).data
    assert response.data == serialized_data

    # Send POST request to the contact_list_view
    new_contact_data = {
        'name': 'New Contact',
        'phone_number': '5555555555',
        'email': 'new.contact@example.com',
        'category': 'OTHER'
    }
    response = api_client.post(url, data=new_contact_data)

    # Check the response status code and data
    assert response.status_code == status.HTTP_201_CREATED
    assert Contact.objects.filter(name='New Contact').exists()
    assert response.data['name'] == 'New Contact'
    assert response.data['phone_number'] == '5555555555'
    assert response.data['email'] == 'new.contact@example.com'
    assert response.data['category'] == 'OTHER'

    # Send POST request with invalid data to the contact_list_view
    invalid_contact_data = {
        'name': 'Invalid Contact',
        'phone_number': '1234567890',  # Existing phone number, should cause validation error
        'email': 'invalid.contact@example.com',
        'category': 'OTHER'
    }
    response = api_client.post(url, data=invalid_contact_data)

    # Check the response status code and data
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not Contact.objects.filter(name='Invalid Contact').exists()



@pytest.mark.django_db
def test_contact_detail_view(api_client):
    # Create a test contact
    contact = Contact.objects.create(name='John Doe', phone_number='1234567890', email='john.doe@example.com',
                                     category='FRIEND')

    # Send GET request to the contact_detail_view
    url = reverse('contact', kwargs={'id': contact.id})
    response = api_client.get(url)

    # Check the response status code and data
    assert response.status_code == status.HTTP_200_OK
    serialized_data = ContactListSerializer(contact).data
    assert response.data == serialized_data

    # Send PUT request to the contact_detail_view
    updated_contact_data = {
        'name': 'Updated Contact',
        'phone_number': '5555555555',
        'email': 'updated.contact@example.com',
        'category': 'OTHER'
    }
    response = api_client.put(url, data=updated_contact_data)

    # Check the response status code and data
    assert response.status_code == status.HTTP_200_OK
    assert Contact.objects.filter(name='Updated Contact').exists()
    assert response.data['name'] == 'Updated Contact'
    assert response.data['phone_number'] == '5555555555'
    assert response.data['email'] == 'updated.contact@example.com'
    assert response.data['category'] == 'OTHER'

    # Send DELETE request to the contact_detail_view
    response = api_client.delete(url)

    # Check the response status code and database deletion
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Contact.objects.filter(id=contact.id).exists()