from yahooquery import Ticker

modules = 'fundPerformance defaultKeyStatistics fundProfile topHoldings quoteType'
ticker = 'XVV'
fund = Ticker([ticker])

fund = fund.get_modules(modules).get(ticker)

top_holdings = [fund['topHoldings']]

# for k, v in pedix.items():
#     print(k, v,'\n')
# # for d in dir(pedix):
# #     print(d)

def get_holdings(top_holdings):
    equity_tickers = map(lambda x: x.get('holdings', {}), top_holdings)
    equity_tickers = {holding.get('symbol')
                        for group in equity_tickers for holding in group}
    return equity_tickers

def getHolderNames(fund_equities):
    """
    Get the names of the fund holders of the equities
    """
    fund_equities = Ticker(list(fund_equities), asynchronous=True, validate=True)
    fund_equities = fund_equities.get_modules('fundOwnership').values()
    fund_equities = filter(lambda x: isinstance(x, dict), fund_equities)
    fund_equities = [fund.get('ownershipList', {}) for fund in fund_equities]
    fund_equities = [f for fund in fund_equities for f in fund] # flatten list
    fund_equities = map(lambda x: x.get('organization', {}), fund_equities)
    return fund_equities


def get_equities(fund_equities):
    fund_equities = Ticker(list(fund_equities), asynchronous=True, validate=True)
    fund_equities = fund_equities.get_modules('fundOwnership').values()
    fund_equities = filter(lambda x: isinstance(x, dict), fund_equities)
    fund_equities = [fund.get('ownershipList', {}) for fund in fund_equities]
    fund_equities = [f for fund in fund_equities for f in fund] # flatten list
    fund_equities = map(lambda x: x.get('organization', {}), fund_equities)


for k, v in fund.items():
    print(k, v, '\n')