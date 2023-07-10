import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_contact_list_url(client):
    """Test that the contact list URL is accessible."""
    url = reverse("contacts")
    response = client.get(url)
    assert response.status_code == 200

