
from django.urls import path,include
from .views.views import contact_list_view, contact_detail_view, index, addContact, create_contact, contact_profile, edit_contact,delete_contact


urlpatterns = [
       path('index/', index, name='index'),
       path('add-contact/', addContact, name='add-contact'),
       path('create-contact/', create_contact, name='create-contact'),
       path('contact-profile/<int:id>/', contact_profile, name='contact-profile'),
       path('contact/<int:id>/edit/', edit_contact, name='edit-contact'),
       path('contact/<int:id>/delete/', delete_contact, name='delete-contact'),
       path("", contact_list_view, name="contacts"),
       path("<int:id>", contact_detail_view, name="contact"),
   
]
