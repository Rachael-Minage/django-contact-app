# Generated by Django 4.2.3 on 2023-07-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("FRIEND", "FRIEND"),
                            ("FAMILY", "FAMILY"),
                            ("WORK", "WORK"),
                            ("OTHER", "OTHER"),
                        ],
                        max_length=25,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
