# Generated by Django 4.1.5 on 2023-04-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("betteretf", "0004_alter_yahooraw_ticker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="holdingsbreakdown",
            name="holding_ticker",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="holdingsbreakdown",
            name="holding_weight",
            field=models.DecimalField(decimal_places=4, max_digits=6, null=True),
        ),
    ]