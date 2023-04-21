from betteretf.models import Fund, YahooRaw
from django.views.generic import ListView
from betteretf.helpers.matching import matcher
from betteretf.helpers.ImportYahooRaw import importYahooRaw


class fundCreateMixin():
    """
    mixin that creates a ticker in the database
    """
    def createFund(self, ticker):
        """
        pull data from yahoo finance and write it to YahooRaw,
        then related convert YahooRaw objects to Fund objects,
        then return the Fund object
        @param ticker: ticker of the fund to be created
        @return: Fund object
        """
        importer = importYahooRaw()
        tickers = importer.graphImport(ticker)
        if tickers == None:
            return
        imported_funds = YahooRaw.objects.filter(ticker__in=tickers)
        converted_funds = map(lambda x: x.convertToFund(), imported_funds)
        converted_funds = [*converted_funds]

    # take input from user

class tickerMatchMixin():
    """
    mixin that matches a ticker in the database
    """
    def matchFund(self, ticker):
        """
        match a ticker in the database
        @param ticker: ticker of the fund to be matched
        @return: list of similar funds
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
        ticker = self.request.GET.get('ticker')
        if ticker is not None and ticker != '':
            ticker = ticker.upper().strip()
            fund  = Fund.objects.filter(ticker=ticker)
            if fund.exists():
                return fund
            else:
                result = self.createFund(ticker)
                if result is None:
                    return None
                fund  = Fund.objects.filter(ticker=ticker)
                return fund

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_fund = self.get_queryset()
        if user_fund is not None and user_fund.exists() and None not in (user_fund[0].beta, user_fund[0].exp_ratio):
            user_fund = user_fund[0]
            context['similar_funds'] = self.matchFund(user_fund.ticker)
        else:
            context['similar_funds'] = None
        return context