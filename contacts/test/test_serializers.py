import pytest
from datetime import datetime
from django.utils.timezone import make_aware
from contacts.serializers import ContactListSerializer
from contacts.models import Contact
from datetime import datetime, timezone

@pytest.fixture
def contact_data():
    return {
        'name': 'David Mensah',
        'phone_number': '1234567890',
        'email': 'david@example.com',
        'category': 'FRIEND',
        'created_at': make_aware(datetime(2023, 7, 10, 18, 17, 27))
    }

@pytest.mark.django_db
def test_contact_list_serializer(contact_data):
    serializer = ContactListSerializer(data=contact_data)
    assert serializer.is_valid(), "Serializer should be valid"

    contact = serializer.save()
    assert Contact.objects.filter(id=contact.id).exists(), "Contact object should be saved in the database"

    # Ensure the serialized data matches the input data
    serialized_data = serializer.data
    assert serialized_data['name'] == contact_data['name'], "Name should match"
    assert serialized_data['phone_number'] == contact_data['phone_number'], "Phone number should match"
    assert serialized_data['email'] == contact_data['email'], "Email should match"
    assert serialized_data['category'] == contact_data['category'], "Category should match"
    serialized_created_at = contact_data['created_at'].replace(tzinfo=timezone.utc)
    assert serialized_created_at == contact_data['created_at'], "Created at should match"


    # ID field should be included in the serialized data
    assert 'id'  in serialized_data, "ID should be included in the serialized data"

    # Ensure read-only fields are not allowed in the input data
    invalid_data = contact_data.copy()
    invalid_data['id'] = 123
    invalid_serializer = ContactListSerializer(data=invalid_data)
    assert not invalid_serializer.is_valid(), "Serializer should be invalid for read-only field"

    # Ensure required fields are validated
    required_fields = ['name', 'phone_number', 'email', 'category']
    for field in required_fields:
        invalid_data = contact_data.copy()
        invalid_data[field] = None
        invalid_serializer = ContactListSerializer(data=invalid_data)
        assert not invalid_serializer.is_valid(), f"Serializer should be invalid for missing {field}"
