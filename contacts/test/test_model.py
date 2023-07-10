import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from contacts.models import Contact
import datetime

@pytest.mark.django_db
def test_create_valid_contact():
    # Create a valid Contact object
    contact = Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='FRIEND'
    )

    # Assert that the object is created successfully
    assert contact.id is not None
    assert contact.name == 'David Mensah'
    assert contact.email == 'davide@test.com'
    assert contact.phone_number == '1234567890'
    assert contact.category == 'FRIEND'
    assert isinstance(contact.created_at, datetime.datetime)
    assert isinstance(contact.updated_at, datetime.datetime)


@pytest.mark.django_db
def test_create_duplicate_email():
    # Create a valid Contact object
    Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='FRIEND'
    )

    # Attempt to create another Contact with the same email
    with pytest.raises(IntegrityError):
        Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='WORK'
        )


@pytest.mark.django_db
def test_create_duplicate_phone_number():
    # Create a valid Contact object
    Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='WORK'
    )

    # Attempt to create another Contact with the same phone number
    with pytest.raises(IntegrityError):
        Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='FRIEND'
        )


@pytest.mark.django_db
def test_create_invalid_category():
    # Attempt to create a Contact with an invalid category value
    with pytest.raises(ValidationError):
        print('i am here')
        contact = Contact.objects.create(
        name='David Mensah',
        email='davide@test.com',
        phone_number='1234567890',
        category='INVALID_CATEGORY'
            
        )
        contact.full_clean()
        contact.save()