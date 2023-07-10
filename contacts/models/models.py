from django.db import models


# Create your models here.
class Contact(models.Model):
    CATEGORY_OPTION = [ 
        ('FRIEND','FRIEND'),
        ('FAMILY','FAMILY'),
        ('WORK','WORK'),
        ('OTHER','OTHER'),

    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,unique=True)
    category = models.CharField(choices=CATEGORY_OPTION,max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.name},{self.phone_number}'
