
from django.urls import path,include
from contacts.views.views import contact_list_view,contact_detail_view

urlpatterns = [
       path("", contact_list_view, name="contacts"),
       path("<int:id>", contact_detail_view, name="contact"),
   
]
