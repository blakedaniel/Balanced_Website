import django
django.setup()

import yahooquery as yq
import multiprocessing
from betteretf.models import YahooRaw

class importYahooRaw:
    def __init__(self):
        self.test_tickers = ('VOO', 'AMJ', 'XLK', 'CWMAX',
                             'FCNTX', 'HLEIX', 'VITSX', 'CAIFX', 'FNCFX')
    
    # pull from api
    def graphImport(self, tickers, batch_size=500):
        if isinstance(tickers, str):
            tickers = [tickers]
        fund_modules = 'fundPerformance defaultKeyStatistics fundProfile topHoldings quoteType'
        funds = yq.Ticker(tickers, asynchronous=True, validate=True)
        funds = [*funds.get_modules(fund_modules).items()]


        if str(funds).find('topHoldings') == -1:
            return None
        if len(funds) > 1:
            with multiprocessing.Pool() as pool:
                results = pool.map(self._convertToYahooRaw, funds, batch_size)
                fund_equities = self._grabEquities(results)
        else:
            results = [self._convertToYahooRaw(funds[0])]
            fund_equities = self._grabEquities(results)
    
        fund_equities = self._getHolderNames(fund_equities)
        fund_equities = list({fund for fund in fund_equities}) # flatten list
        fund_tickers = self._getTickers(fund_equities, batch_size)
        fund_tickers = fund_tickers.difference(set(tickers)) # remove original tickers

        fund_tickers = list(fund_tickers)

        fund_tickers = map(self._checkExists, fund_tickers)
        fund_tickers = filter(lambda x: x is not None, fund_tickers)
        fund_tickers = list(fund_tickers)
        if len(fund_tickers) == 0:
            return tickers

        fund_holders = yq.Ticker(fund_tickers, asynchronous=True, validate=True)
        fund_holders = fund_holders.get_modules(fund_modules).items()
        with multiprocessing.Pool() as pool:
            results += pool.map(self._convertToYahooRaw, fund_holders, batch_size)
            results = filter(lambda x: isinstance(x, YahooRaw), results)
        fund_tickers += tickers
        fund_tickers = list(set(fund_tickers))
        return fund_tickers


    # transform into correct format
    def _convertToYahooRaw(self, funds_data):
        """
        Convert the data from the yahooquery api into the YahooRaw model object
        """
        ticker = funds_data[0]
        fund_data = funds_data[1]
        if isinstance(fund_data, str):
            return

        # TODO: update this to be just create() instead of update_or_create()

        yahoo_raw = YahooRaw.objects.update_or_create(
            ticker=ticker,
            quote_type=fund_data.get('quoteType', {}),
            fund_performance=fund_data.get('fundPerformance', {}),
            default_key_statistics=fund_data.get('defaultKeyStatistics', {}),
            fund_profile=fund_data.get('fundProfile', {}),
            top_holdings=fund_data.get('topHoldings', {}),
        )
        return yahoo_raw[0]


    def _grabEquities(self, top_holdings):
        """
        Grab the equities from the top holdings of the funds
        @param top_holdings: list of top holdings of the funds
        @return: set of equity tickers
        """
        equity_tickers = map(lambda x: x.top_holdings.get('holdings'), top_holdings)
        equity_tickers = {holding.get('symbol') for group in equity_tickers for holding in group}
        return equity_tickers


    def _checkExists(self, ticker):
        """
        Check if the ticker already exists in the database
        """
        fund  = YahooRaw.objects.filter(ticker=ticker)
        if not fund.exists():
            return ticker
            

    def _getHolderNames(self, fund_equities):
        """
        Get the names of the fund holders of the equities
        """
        fund_equities = yq.Ticker(list(fund_equities), asynchronous=True, validate=True)
        fund_equities = fund_equities.get_modules('fundOwnership').values()
        fund_equities = filter(lambda x: isinstance(x, dict), fund_equities)
        fund_equities = [fund.get('ownershipList', {}) for fund in fund_equities]
        fund_equities = [f for fund in fund_equities for f in fund] # flatten list
        fund_equities = map(lambda x: x.get('organization', {}), fund_equities)
        return fund_equities

    def _getTickers(self, fund_equities, batch_size=500):
        """
        Get the fund tickers of holders of the equities
        @param fund_equities: list of fund holders of the equities
        @param batch_size: size of the batch to be processed
        @return: set of fund tickers
        """       
        with multiprocessing.Pool() as pool:
            fund_equities = list(fund_equities)
            batch_size = max(batch_size//50, 5)
            fund_tickers = []
            while len(fund_equities) > batch_size: 
                batch, fund_equities = fund_equities[:batch_size], fund_equities[batch_size:]
                fund_tickers.extend(pool.map(self._getFund, batch))
            if len(fund_equities) > 0:
                fund_tickers.extend(pool.map(self._getFund, fund_equities))
            fund_tickers = map(lambda x: x.get('symbol'), fund_tickers)
            fund_tickers = filter(lambda x: x is not None, fund_tickers)
            fund_tickers = set(fund_tickers)
        return fund_tickers


    def _getFund(self, equity_holder):
        """
        Get the fund details of the equity holder
        """
        try:
            results = yq.search(equity_holder, first_quote=True)
            return results
        except:
            return
