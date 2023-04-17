from django.shortcuts import get_object_or_404, HttpResponse, render
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory
from django.views.generic import ListView, CreateView
from betteretf.helpers.BulkStockImport import Importer
from betteretf.helpers.matching import matcher
from betteretf.helpers.ImportYahooRaw import importYahooRaw
from asgiref.sync import sync_to_async


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
        pull data from yahoo finance and write it to YahooRaw,
        then related convert YahooRaw objects to Fund objects,
        then return the Fund object
        param ticker: ticker of the fund to be created
        return: Fund object
        """
        bsi = Importer()
        # create a new ticker
        bsi.bulkImport([ticker], holders=True)

        # get the ticker from the database
        fund = Fund.objects.get(ticker=ticker)
        # search for similar tickers
        import_related = importYahooRaw().graphImport([ticker])
        # search through yahoo raw data for similar tickers
        # import related tickers into Fund model
        # get similar tickers and return them
        
        return fund
    # take input from user

class tickerMatchMixin():
    """
    mixin that matches a ticker in the database
    """
    def matchFund(self, ticker):
        """
        match a ticker in the database
        """
        # get the ticker from the database
        fund = Fund.objects.get(ticker=ticker)
        # get similar tickers
        similar_funds = matcher(fund)
        similar_funds = similar_funds.match()
        return similar_funds


class tickerSearchView(fundCreateMixin, tickerMatchMixin, ListView):
    """
    view that searches for a ticker in the database and either returns it or creates it
    """
    model = Fund
    template_name = 'home.html'
    context_object_name = 'user_fund'

    def get_queryset(self):
        # get the ticker from GET parameters
        ticker = self.request.GET.get('ticker')
        # if fund of ticker is not None, filter the queryset
        if ticker is not None:
            fund  = Fund.objects.filter(ticker=ticker)
            if fund.exists():
                return fund
            else:
                # if fund of ticker does not exist, create it
            # try:
                fund = self.createFund(ticker)
                return fund
            # except:
            #     HttpResponse('Error creating new fund')
            #     return None

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the ticker from the database
        user_fund = self.get_queryset()
        if user_fund is not None and user_fund.exists() and None not in (user_fund[0].beta, user_fund[0].exp_ratio):
            user_fund = user_fund[0]
            context['similar_funds'] = self.matchFund(user_fund.ticker)
        else:
            context['similar_funds'] = None
        return context
