import yahooquery as yq

def fundHolders(fund_ticker):
    fund = yq.Ticker(fund_ticker)  # set initial fund
    # pull top ten equities/funds holdings that make up the fund
    holding_tickers = [ticker for ticker in fund.fund_top_holdings['symbol']]
    # pull list of data on each holding equity/fund
    holding_funds = yq.Ticker(holding_tickers, asynchronous=True)
    # get quoteType and Holdingers for each ticker
    holding_funds = holding_funds.get_modules('quoteType fundOwnership')
    holding_funds = map(holding_funds.get, holding_tickers)

    # pull out quoteType
    func = lambda holding: holding.get('quoteType', {}).get('quoteType', {})
    quote_types = map(func, holding_funds)
    # zip up to ticker, and only go to next phase on those that are Equity

    #pull out owners
    func = lambda holding: holding.get('fundOwnership', {}).get('ownershipList', {})
    fund_owners = map(func, holding_funds)

    funds = set()
    for fund_owner in fund_owners:
        for fund in fund_owner:
            fund = fund.get('organization')
            if fund is not None:
                fund = yq.search(fund, first_quote=True)
                fund = fund.get('symbol')
                if fund != None
                    funds.add(fund)

    return funds