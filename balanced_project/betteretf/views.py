from django.shortcuts import render
from django.shortcuts import get_object_or_404
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory
from django.views.generic import ListView, CreateView
from betteretf.BulkYahooImportMngr import bulkStockImporter


def HomeView(request):
    fund_input = 0 # form input
    fund_matches = 0 # form response

    return render(request, 'betteretf/home.html', {
        'fund_input': fund_input,
        'fund_matches': fund_matches,
    })

class fundCreateMixin():
    """
    mixin that creates a ticker in the database
    """
    def createFund(self, ticker):
        """
        pull data from yahoo finance and create a new ticker
        """
        bsi = bulkStockImporter()
        # create a new ticker
        bsi.bulkImport([ticker])
        # get the ticker from the database
        fund = Fund.objects.get(ticker=ticker)
        return fund
    # take input from user

class tickerSearchView(fundCreateMixin, ListView):
    """
    view that searches for a ticker in the database and either returns it or creates it
    """
    model = Fund
    template_name = 'home.html'
    context_object_name = 'user_fund'

    def get_queryset(self):
        # get the ticker from GET parameters
        ticker = self.request.GET.get('ticker')

        # if ticker is not None, filter the queryset
        if ticker is not None:
            fund = Fund.objects.filter(ticker=ticker)
            if fund.exists():
                return fund
            else:
                # if ticker does not exist, create it
                try:
                    fund = self.createFund(ticker)
                    return fund
                except:
                    return None
            
class betterTickerView():
    """
    view that displays similar tickers and their details
    """
    pass