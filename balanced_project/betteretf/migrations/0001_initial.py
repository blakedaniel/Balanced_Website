# Generated by Django 4.1.5 on 2023-04-12 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=8, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('quote_type', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('beta', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('exp_ratio', models.DecimalField(decimal_places=4, max_digits=5, null=True)),
                ('holdings_cat', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('sectors_cat', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('history_cat', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='YahooRaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=8, unique=True)),
                ('fund_performance', models.JSONField()),
                ('default_key_statistics', models.JSONField()),
                ('fund_profile', models.JSONField()),
                ('top_holdings', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ThreeYearHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('open', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='betteretf.fund', to_field='ticker')),
            ],
        ),
        migrations.CreateModel(
            name='SectorsBreakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_materials', models.DecimalField(decimal_places=4, max_digits=6)),
                ('communication_services', models.DecimalField(decimal_places=4, max_digits=6)),
                ('consumer_cyclical', models.DecimalField(decimal_places=4, max_digits=6)),
                ('consumer_defensive', models.DecimalField(decimal_places=4, max_digits=6)),
                ('energy', models.DecimalField(decimal_places=4, max_digits=6)),
                ('financial_services', models.DecimalField(decimal_places=4, max_digits=6)),
                ('healthcare', models.DecimalField(decimal_places=4, max_digits=6)),
                ('industrials', models.DecimalField(decimal_places=4, max_digits=6)),
                ('realestate', models.DecimalField(decimal_places=4, max_digits=6)),
                ('technology', models.DecimalField(decimal_places=4, max_digits=6)),
                ('utilities', models.DecimalField(decimal_places=4, max_digits=6)),
                ('ticker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sectors', to='betteretf.fund', to_field='ticker')),
            ],
        ),
        migrations.CreateModel(
            name='HoldingsBreakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holding_ticker', models.CharField(max_length=10)),
                ('holding_weight', models.DecimalField(decimal_places=4, max_digits=6)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='betteretf.fund', to_field='ticker')),
            ],
        ),
    ]
