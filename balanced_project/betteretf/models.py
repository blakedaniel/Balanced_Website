from django.db import models, IntegrityError

class YahooRaw(models.Model):
    ticker = models.CharField(max_length=25, unique=True)
    quote_type = models.JSONField()
    fund_performance = models.JSONField()
    default_key_statistics = models.JSONField()
    fund_profile = models.JSONField()
    top_holdings = models.JSONField()

    def __str__(self):
        return f'{self.ticker}'
    
    def __repr__(self):
        return f'{self.ticker}'
    
    def convertToFund(self):
        """
        Convert the raw data to a fund model
        """
        org_fund = YahooRaw.objects.filter(ticker=self.ticker)
        org_fund = org_fund.values('quote_type__shortName',
                              'quote_type__quoteType',
                              'fund_profile__categoryName',
                              'default_key_statistics__beta3Year',
                              'fund_profile__feesExpensesInvestment__annualReportExpenseRatio',
                              'top_holdings__holdings',
                              'fund_performance__riskOverviewStatisticsCat__riskStatisticsCat'
                              ).first()

        beta = org_fund['default_key_statistics__beta3Year']
        # breakpoint()
        if beta == 0:
            try:
                beta = org_fund['fund_performance__riskOverviewStatisticsCat__riskStatisticsCat']
                beta = beta[0]['beta']
            except:
                beta = 0

        if self.ticker in ('BGRFX', 'BARAX'):
            breakpoint()

        fund = Fund.objects.update_or_create(
            ticker=self.ticker,
            name = org_fund['quote_type__shortName'],
            quote_type = org_fund['quote_type__quoteType'],
            category = org_fund['fund_profile__categoryName'],
            beta = beta,
            exp_ratio = org_fund['fund_profile__feesExpensesInvestment__annualReportExpenseRatio'],
        )

        # convert holdings of YahooRaw object to HoldingsBreakdown object
        holdings_breakdown = org_fund['top_holdings__holdings']
        try:

            holdings_breakdown = map(lambda x: self._convertToHoldings(fund[0], x),
                                    holdings_breakdown)
            HoldingsBreakdown.objects.bulk_create(tuple(holdings_breakdown))

        except TypeError:

            holdings_breakdown = {'symbol': None, 'holdingPercent': None}
            holdings_breakdown = self._convertToHoldings(fund[0], holdings_breakdown)
            holdings_breakdown.save()

        return fund
    
    def _convertToHoldings(self, ticker, holdings_breakdown):
        holdings_breakdown = HoldingsBreakdown(
            ticker = ticker,
            holding_ticker = holdings_breakdown['symbol'],
            holding_weight = holdings_breakdown['holdingPercent']
        )
        return holdings_breakdown


class Fund(models.Model):
    ticker = models.CharField(max_length=8, unique=True)
    name = models.TextField()
    quote_type = models.CharField(max_length=50)
    category = models.CharField(max_length=100, null=True, blank=True)

    beta = models.DecimalField(max_digits=5,
                               decimal_places=2,
                               blank=True,
                               null=True)
    
    exp_ratio = models.DecimalField(max_digits=5, decimal_places=4, null=True)
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
    ticker = models.ForeignKey(Fund,
                               on_delete=models.CASCADE,
                               related_name='holdings',
                               to_field='ticker')
    
    holding_ticker = models.CharField(max_length=10, null=True)
    holding_weight = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    
    def __str__(self):
        return f'{self.ticker} - {self.holding_ticker}'


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



