import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from contacts.models.models import Contact
from contacts.serializers import ContactListSerializer
from django.test import Client
from contacts.forms.forms import ContactForm, EditContactForm

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client():
    return Client()

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



@pytest.fixture
def create_contact():
    def _create_contact(name, email, phone_number, category):
        return Contact.objects.create(name=name, email=email, phone_number=phone_number, category=category)
    return _create_contact    


@pytest.mark.django_db
def test_index_view(client, create_contact):
    contact1 = create_contact(name='John Doe', email='john@example.com', phone_number='1234567890', category='Friends')
    contact2 = create_contact(name='Jane Smith', email='jane@example.com', phone_number='9876543210', category='Work')

    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200
    assert 'contacts' in response.context
    assert len(response.context['contacts']) == 2
    assert contact1 in response.context['contacts']
    assert contact2 in response.context['contacts']


@pytest.mark.django_db
def test_add_contact_view(client):
    url = reverse('add-contact')
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_add_contact_view(client):
    url = reverse('add-contact')
    response = client.get(url)

    assert response.status_code == 200





@pytest.mark.django_db
def test_contact_profile_view(client, create_contact):
    contact = create_contact(name='John Doe', email='john@example.com', phone_number='1234567890', category='Friends')

    url = reverse('contact-profile', args=[contact.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'contact' in response.context
    assert response.context['contact'] == contact

    