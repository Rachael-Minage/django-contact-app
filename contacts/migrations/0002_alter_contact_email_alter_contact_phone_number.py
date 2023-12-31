# Generated by Django 4.2.3 on 2023-07-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="phone_number",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
