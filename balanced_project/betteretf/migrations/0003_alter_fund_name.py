# Generated by Django 4.1.5 on 2023-04-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("betteretf", "0002_yahooraw_quote_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fund",
            name="name",
            field=models.TextField(),
        ),
    ]