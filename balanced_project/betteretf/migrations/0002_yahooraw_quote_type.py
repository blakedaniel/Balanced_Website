# Generated by Django 4.1.5 on 2023-04-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("betteretf", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="yahooraw",
            name="quote_type",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
