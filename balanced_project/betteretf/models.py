from django.db import models

class YahooRaw(models.Model):
    ticker = models.CharField(max_length=8, unique=True)
    data = models.TextField()
    three_year_history = models.JSONField()


class Fund(models.Model):
    ticker = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=100, null=True, blank=True)
    beta = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    exp_ratio = models.DecimalField(max_digits=5, decimal_places=4)
    # update cat fields so they are boolean -- new purpose for them
    # is whether the data exists in the database; meant to highlight 
    # what etfs have been pulled from yahoo
    holdings_cat = models.DecimalField(
        max_digits=5, decimal_places=4, blank=True, null=True)
    sectors_cat = models.DecimalField(
        max_digits=5, decimal_places=4, blank=True, null=   True)
    history_cat = models.DecimalField(
        max_digits=5, decimal_places=4, blank=True, null=True)
    
    def __str__(self):
        return f'{self.ticker}'


class HoldingsBreakdown(models.Model):
    ticker = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='holdings', to_field='ticker')
    holding_ticker = models.CharField(max_length=10)
    holding_weight = models.DecimalField(max_digits=6, decimal_places=4)



class SectorsBreakdown(models.Model):
    ticker = models.OneToOneField(Fund, on_delete=models.CASCADE, related_name='sectors', to_field='ticker')
    basic_materials = models.DecimalField(max_digits=6, decimal_places=4)
    communication_services = models.DecimalField(max_digits=6, decimal_places=4)
    consumer_cyclical = models.DecimalField(max_digits=6, decimal_places=4)
    consumer_defensive = models.DecimalField(max_digits=6, decimal_places=4)
    energy = models.DecimalField(max_digits=6, decimal_places=4)
    financial_services = models.DecimalField(max_digits=6, decimal_places=4)
    healthcare = models.DecimalField(max_digits=6, decimal_places=4)
    industrials = models.DecimalField(max_digits=6, decimal_places=4)
    realestate = models.DecimalField(max_digits=6, decimal_places=4)
    technology = models.DecimalField(max_digits=6, decimal_places=4)
    utilities = models.DecimalField(max_digits=6, decimal_places=4)



class ThreeYearHistory(models.Model):
    ticker = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='history', to_field='ticker')
    date = models.DateField()
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.ticker} {self.date}'



