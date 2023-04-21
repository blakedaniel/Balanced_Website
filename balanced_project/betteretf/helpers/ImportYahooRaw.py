import yahooquery as yq
from betteretf.helpers.asyncYahooSearch import search
from betteretf.models import YahooRaw


class importYahooRaw:
    """
    import raw data from yahoo finance
    """
    def __init__(self):
        self.test_tickers = (
            "VOO",
            "AMJ",
            "XLK",
            "CWMAX",
            "FCNTX",
            "HLEIX",
            "VITSX",
            "CAIFX",
            "FNCFX",
        )

    def graphImport(self, tickers, batch_size=500):
        """
        import a ticker and all of its related tickers
        @param tickers: ticker or list of tickers to be imported
        @param batch_size: number of tickers to be imported at a time
        @return: list of tickers that were imported
        """
        # Convert to list if necessary
        if isinstance(tickers, str):
            tickers = [tickers]

        # Get the modules from the ticker
        fund_modules = (
            "fundPerformance defaultKeyStatistics fundProfile topHoldings quoteType"
        )
        funds = yq.Ticker(tickers, asynchronous=True, validate=True)
        funds = [*funds.get_modules(fund_modules).items()]

        # Check if the top holdings module is present
        if str(funds).find("topHoldings") == -1:
            return None

        # Get the results from the ticker
        if len(funds) > 1:
            results = map(self._convertToYahooRaw, funds)
            fund_equities = self._grabEquities(results)
        else:
            results = [self._convertToYahooRaw(funds[0])]
            fund_equities = self._grabEquities(results)

        # Get the holders of the stock
        fund_equities = self._getHolderNames(fund_equities)
        fund_equities = list({fund for fund in fund_equities})

        # Validate the tickers
        if self._validate(fund_equities):
            return tickers

        # Get the tickers from the equities
        fund_tickers = self._getTickers(fund_equities, batch_size)
        fund_tickers = list(fund_tickers)

        # Check if the tickers exist
        fund_tickers = map(self._checkExists, fund_tickers)
        fund_tickers = filter(lambda x: x is not None, fund_tickers)
        fund_tickers = list(fund_tickers)

        # Validate the tickers
        if self._validate(fund_tickers):
            return tickers

        # Get the ticker from the modules
        fund_holders = yq.Ticker(fund_tickers, asynchronous=True, validate=True)
        fund_holders = fund_holders.get_modules(fund_modules).items()

        # Get the results of the tickers
        results += map(self._convertToYahooRaw, fund_holders)
        results = filter(lambda x: isinstance(x, YahooRaw), results)

        # Add the tickers to the list
        fund_tickers += tickers
        fund_tickers = list(set(fund_tickers))
        return fund_tickers

    def _validate(self, list_set_tuple):
        return len(list_set_tuple) == 0

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
            quote_type=fund_data.get("quoteType", {}),
            fund_performance=fund_data.get("fundPerformance", {}),
            default_key_statistics=fund_data.get("defaultKeyStatistics", {}),
            fund_profile=fund_data.get("fundProfile", {}),
            top_holdings=fund_data.get("topHoldings", {}),
        )
        return yahoo_raw[0]

    def _grabEquities(self, top_holdings, new=True):
        """
        Grab the equities from the top holdings of the funds
        @param top_holdings: list of top holdings of the funds
        @return: set of equity tickers
        """
        equity_tickers = map(lambda x: x.top_holdings.get("holdings"), top_holdings)
        equity_tickers = {
            holding.get("symbol") for group in equity_tickers for holding in group
        }
        return equity_tickers

    def _checkExists(self, ticker):
        """
        Check if the ticker already exists in the database
        """
        fund = YahooRaw.objects.filter(ticker=ticker)
        if not fund.exists():
            return ticker

    def _getHolderNames(self, fund_equities):
        """
        Get the names of the fund holders of the equities
        """
        fund_equities = yq.Ticker(list(fund_equities), asynchronous=True, validate=True)
        fund_equities = fund_equities.get_modules("fundOwnership").values()
        fund_equities = filter(lambda x: isinstance(x, dict), fund_equities)
        fund_equities = [fund.get("ownershipList", {}) for fund in fund_equities]
        fund_equities = [f for fund in fund_equities for f in fund]  # flatten list
        fund_equities = map(lambda x: x.get("organization", {}), fund_equities)
        return fund_equities

    def _getTickers(self, fund_equities, batch_size=500):
        """
        Get the fund tickers of holders of the equities
        @param fund_equities: list of fund holders of the equities
        @param batch_size: size of the batch to be processed
        @return: set of fund tickers
        """
        fund_equities = list(fund_equities)
        fund_tickers = []
        fund_tickers.extend(search(fund_equities))
        if len(fund_equities) > 0:
            fund_tickers.extend(search(fund_equities))
        fund_tickers = map(lambda x: x.get("symbol"), fund_tickers)
        fund_tickers = filter(lambda x: x is not None, fund_tickers)
        fund_tickers = set(fund_tickers)
        return fund_tickers

