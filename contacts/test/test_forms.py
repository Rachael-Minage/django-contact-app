import pytest
from contacts.models.models import Contact
from contacts.forms.forms import ContactForm, EditContactForm
from django.db import IntegrityError

@pytest.fixture
def valid_contact_data():
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone_number': '1234567890',
        'category': 'FRIEND'
    }


@pytest.fixture
def invalid_contact_data():
    return {
        'name': '',  # Invalid: Name is required
        'email': 'invalid_email',  # Invalid: Email format is incorrect
        'phone_number': '123',  # Invalid: Phone number is too short
        'category': 'Unknown'  # Invalid: Category value is not allowed
    }


@pytest.mark.django_db
def test_contact_form_valid(valid_contact_data):
    form = ContactForm(data=valid_contact_data)
    assert form.is_valid(), form.errors

@pytest.mark.django_db
def test_contact_form_invalid(invalid_contact_data):
    form = ContactForm(data=invalid_contact_data)

    print(form.errors)
    print(form.cleaned_data['phone_number'])
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'email' in form.errors
    assert 'category' in form.errors

@pytest.mark.django_db
def test_edit_contact_form_valid(valid_contact_data):
    form = EditContactForm(data=valid_contact_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_edit_contact_form_invalid(invalid_contact_data):
    form = EditContactForm(data=invalid_contact_data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'email' in form.errors
    assert 'category' in form.errors
