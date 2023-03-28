from django.shortcuts import render
from django.shortcuts import get_object_or_404
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory
from django.views.generic import ListView
from betteretf.BulkYahooImportMngr import bulkStockImporter


def HomeView(request):
    fund_input = 0 # form input
    fund_matches = 0 # form response

    return render(request, 'betteretf/home.html', {
        'fund_input': fund_input,
        'fund_matches': fund_matches,
    })

class FundViewSet(ListView):
    model = Fund
    template_name = 'betteretf/fund_list.html'

    def get_object(self, user_ticker):
        obj = super().get_object()
        obj = Fund.objects.get(ticker = user_ticker)
        if obj.DoesNotExist():
            # run the bulk import code for a single ticker
            bsi = bulkStockImporter()
            bsi.createTickers([user_ticker])
            bsi.createTickerDetails([user_ticker])
            obj = Fund.objects.get(ticker = user_ticker)
            return obj
        else:
            return obj

    def tickerFilter(self, user_ticker):
        # user_ticker is the ticker provided by the user
        # user_ticker.beta is the beta of the ticker provided by the user
        # user_ticker.sector is the set of sector weights of the ticker provided by the user
        # user_ticker.holdings is the set of holdings of the ticker provided by the user
        queryset = Fund.objects.all()
        self.similar_beta = queryset.filter(beta__gte=user_ticker.beta * .99, beta__lte=user_ticker.beta * 1.01)
        self.similar_beta = set(self.similar_beta)

        # for the ticker provided, find all funds with at least 80% of the same holdings
        similar_holdings = queryset.all()