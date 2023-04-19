import yahooquery as yq
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory
from collections import defaultdict
from django.db import transaction
import pandas as pd

# TODO: add error handling throughout

class Importer(object):
    def __init__(self):
        self.chunk_size = 500
        self.further_actions = defaultdict(list)
        pass

    def filesImport(self):
        """
        Import all files in the import folder.
        """
        files = []
        self.tickers = []
        more_input = 'y'
        while more_input == 'y':
            file_input = input("Enter path/name of file to import: ")
            symbol_input = input("Enter column name of ticker symbol: ")
            files.append((file_input, symbol_input))
            more_input = input("More files in import (y/n): ")

        for file in files:
            with open(file[0], 'r') as f:
                tickers = pd.read_csv(f)[[symbol_input]]
                tickers = tickers.to_dict('list')[symbol_input]
                self.tickers.extend(tickers)


    def _createTicker(self, fund_ticker, response):
        name = None
        quote_type = None
        category = None
        beta = None
        exp_ratio = None


        if isinstance(dict, response.quote_type[fund_ticker]):
            name = response.quote_type[fund_ticker].get('shortName', None)
            quote_type = response.quote_type[fund_ticker].get('quoteType', None)
        
        if isinstance(dict, response.key_stats[fund_ticker]):
            category = response.key_stats[fund_ticker].get('category', None)
            
        if isinstance(dict, response.fund_performance[fund_ticker]):
            beta = response.fund_performance[fund_ticker].get('riskOverviewStatistics', {}).get('riskStatistics', {})[0].get('beta', None)
            
        if isinstance(dict, response.fund_profile[fund_ticker]):
            exp_ratio = response.fund_profile[fund_ticker].get('feesExpensesInvestment', {}).get('annualReportExpenseRatio', None)
            
        print(f'Fund created for ticker: {fund_ticker}')

        fund= Fund(ticker = fund_ticker,
                   name = name,
                   quote_type = quote_type,
                   category = category,
                   beta = beta,
                   exp_ratio = exp_ratio)
        return [fund]

    @transaction.atomic
    def createTickers(self, tickers=None):
        """
        Add basic details of a ticker to the database, for a list of tickers. Returns
        error if ticker already exists in database.
        """
        if tickers is None:
            tickers = self.tickers
    
        funds = []
        for ticker in tickers:
            response = yq.Ticker(ticker)
            if Fund.objects.filter(ticker = ticker).exists():
                print(f'Fund already exists for ticker: {ticker}')
            else:
                ct_response = self._createTicker(ticker, response)
                if ct_response == 'error':
                    self.further_actions['for_removal'].append(ticker)
                    continue
                else:
                    funds.extend(ct_response)

        Fund.objects.bulk_create(funds, batch_size=self.chunk_size)
        print('Bulk create complete\n')


    def _createHoldings(self, fund_ticker, response):
        h = None
        try:
            holdings = response.fund_top_holdings[['symbol', 'holdingPercent']]
            print(f'HoldingsBreakdown created for ticker: {fund_ticker}')
        except:
            print(f'No holdings data: {fund_ticker}')
            return h
        holdings = holdings.to_dict('index')
        h = []
        for k, v in holdings.items():
            holding = HoldingsBreakdown(ticker = Fund.objects.get(ticker = fund_ticker),
                                        holding_ticker = v['symbol'],
                                        holding_weight = v['holdingPercent'])
            h.append(holding)
        return h


    def _createSectors(self, fund_ticker, response):
        sectors = response.fund_sector_weightings
        if type(sectors[fund_ticker]) != type({}):
            print(f'No sector data: {fund_ticker}')
            return None
        else:
            sectors = response.fund_sector_weightings
            print(f'SectorsBreakdown created for ticker: {fund_ticker}')
            return sectors
        sectors = sectors.to_dict('index')
        sector = SectorsBreakdown(ticker = Fund.objects.get(ticker = fund_ticker),
                                    basic_materials = sectors['basic_materials'][fund_ticker],
                                    communication_services = sectors['communication_services'][fund_ticker],
                                    consumer_cyclical = sectors['consumer_cyclical'][fund_ticker],
                                    consumer_defensive = sectors['consumer_defensive'][fund_ticker],
                                    energy = sectors['energy'][fund_ticker],
                                    financial_services = sectors['financial_services'][fund_ticker],
                                    healthcare = sectors['healthcare'][fund_ticker],
                                    industrials = sectors['industrials'][fund_ticker],
                                    realestate = sectors['realestate'][fund_ticker],
                                    technology = sectors['technology'][fund_ticker],
                                    utilities = sectors['utilities'][fund_ticker])
        return [sector]


    def _createHistory(self, fund_ticker, response):
        h = None
        if isinstance(dict, response.history(start='2019-01-01', end='2022-12-31')[fund_ticker]):
            history = response.history(start='2019-01-01', end='2022-12-31')[['open', 'high', 'low', 'close']]
            print(f'ThreeYearHistory created for ticker: {fund_ticker}')
        else:
            print(f'No history data: {fund_ticker}')
            return h
        history = history.to_dict('index')
        for k, v in history.items():
            day = ThreeYearHistory(ticker = Fund.objects.get(ticker = fund_ticker),
                                        date = k[1].strftime('%Y-%m-%d'),
                                        high = v['high'],
                                        low = v['low'],
                                        open = v['open'],
                                        close = v['close'])
            h.append(day)
        return h

    @transaction.atomic
    def createTickerDetails(self, tickers=None):
        """
        Add details of a ticker to the database, for a list of tickers. Details include:
        holdings breakdown; sectors breakdown; 3 year history. Ticker must already exist
        in database.
        """
        if tickers is None:
            tickers = self.tickers

        # remove problem tickers before proceeding
        for ticker in self.further_actions['for_removal']:
            try:
                tickers.remove(ticker)
            except:
                continue

        details = defaultdict(list)
        for ticker in tickers:
            response = yq.Ticker(ticker)

            if HoldingsBreakdown.objects.filter(ticker = ticker).exists():
                print('HoldingsBreakdown already exists for ticker: {}'.format(ticker))
            else:
                holdings = self._createHoldings(ticker, response)
                if holdings is None:
                    details['holdings'].extend([])
                else:
                    details['holdings'].extend(holdings)

            if SectorsBreakdown.objects.filter(ticker = ticker).exists():
                print('SectorsBreakdown already exists for ticker: {}'.format(ticker))
            else:
                sectors = self._createSectors(ticker, response)
                if sectors is None:
                    details['sectors'].extend([])
                else:
                    details['sectors'].extend(sectors)
                
            if ThreeYearHistory.objects.filter(ticker = ticker).exists():
                print('ThreeYearHistory already exists for ticker: {}'.format(ticker))
            else:
                history = self._createHistory(ticker, response)
                if history is None:
                    details['history'].extend([])
                else:
                    details['history'].extend(history)
        
        HoldingsBreakdown.objects.bulk_create(details['holdings'], batch_size=self.chunk_size)
        SectorsBreakdown.objects.bulk_create(details['sectors'], batch_size=self.chunk_size)
        ThreeYearHistory.objects.bulk_create(details['history'], batch_size=self.chunk_size)
        print('\nTicker details have been completed.')


    def fundHolders(self, fund_ticker):
        fund = yq.Ticker(fund_ticker)  # set initial fund
        # pull top ten equities/funds holdings that make up the fund
        holding_tickers = [ticker for ticker in fund.fund_top_holdings['symbol']]
        # pull list of data on each holding equity/fund
        holding_funds = yq.Ticker(holding_tickers, asynchronous=True)
        # get quoteType and Holdingers for each ticker
        holding_funds = holding_funds.get_modules('quoteType fundOwnership')
        holding_funds = map(holding_funds.get, holding_tickers)

        # pull out quoteType
        def func(holding): holding.get('quoteType', {}).get('quoteType', {})
        map(func, holding_funds)
        # zip up to ticker, and only go to next phase on those that are Equity

        #pull out owners
        def func(holding): holding.get('fundOwnership', {}).get('ownershipList', {})
        fund_owners = map(func, holding_funds)

        funds = set()
        for fund_owner in fund_owners:
            for fund in fund_owner:
                fund = fund.get('organization')
                if fund is not None:
                    fund = yq.search(fund, first_quote=True)
                    funds.add(fund.get('symbol'))
        return funds


    def bulkImport(self, tickers=None, holders=False):
        """
        Bulk import tickers and details to database.
        """
        if tickers is None:
            tickers = set(self.tickers)
        else:
            tickers = set(tickers)

        if holders:
            try:
                holder_funds = map(self.fundHolders, tickers)
                merge_tickers = tickers.copy()
                for funds in holder_funds:
                    merge_tickers.update(funds)
                tickers.update(merge_tickers)
                tickers.remove(None)  # need to identify why None is entering set
                # tickers.update(holder_funds)
            except KeyError:
                print('Error while searching for holder information')
            finally:
                self.createTickers(tickers)
                self.createTickerDetails(tickers)
                return

        self.createTickers(tickers)
        self.createTickerDetails(tickers)
        return
