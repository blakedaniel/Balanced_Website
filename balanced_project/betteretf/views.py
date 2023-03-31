from django.shortcuts import render
from django.shortcuts import get_object_or_404
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory
from django.views.generic import ListView, CreateView
from betteretf.helpers.BulkStockImport import importer
from betteretf.helpers.matching import matcher
from betteretf.helpers.TickerOnDemand import fundHolders


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
        bsi = importer()
        # create a new ticker
        bsi.bulkImport([ticker])
        holder_funds = bsi.fundHolders(ticker)
        breakpoint()
        bsi.bulkImport([].extend(holder_funds))

        # get the ticker from the database
        fund = Fund.objects.get(ticker=ticker)
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
                fund = self.createFund(ticker)
                return fund

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the ticker from the database
        user_fund = self.get_queryset()
        if user_fund is not None and user_fund.exists():
            user_fund = user_fund[0]
            context['similar_funds'] = self.matchFund(user_fund.ticker)
        else:
            context['similar_funds'] = None
        return context