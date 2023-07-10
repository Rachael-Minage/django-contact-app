
from django.urls import path,include
from .views import ContactDetailAPIView,ContactListAPIView  

urlpatterns = [
       path("", ContactListAPIView.as_view(), name="contacts"),
       path("<int:id>", ContactDetailAPIView.as_view(), name="contact"),
   
]
