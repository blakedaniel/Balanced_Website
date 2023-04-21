# Balaced
*Financial Literacy Made Easy*

## BetterETF Django App

Demo Site: https://balanced.fly.dev/betteretf/

### [Handy Helper Modules](https://github.com/blakedaniel/Balanced_Website/tree/main/balanced_project/betteretf/helpers)

#### [betteretf.helpers.ImportYahooRaw](https://github.com/blakedaniel/Balanced_Website/blob/main/balanced_project/betteretf/helpers/ImportYahooRaw.py)

This module contains methods for importing raw financial data from Yahoo Finance API for a given list of stock tickers. The `graphImport()` method imports tickers and their related tickers' data, validates them, retrieves data for their top holdings and fund ownership, and converts the data into a custom model object YahooRaw for the BetterETF Djanog App. This is called graphImport, as it does a graph search on a given fund ticker, then identifies all funds that share a similar makeup of funds, then prepares all of these objects for importing. The class also has other private methods that perform helper functions for:

- Validating data throughout the `graphImport()` method.
- Asynchrously retrieving equity tickers of the provided tickers.
- Asynchrously identifying names, tickers and data of funds that include the retrieved tickers.

Overall, this code can be used to automate the process of importing raw financial data from Yahoo Finance API into a custom model object, which can then be used to perform further analysis or integrated into a larger financial system.

#### [betteretf.helpers.asyncYahooSearch](https://github.com/blakedaniel/Balanced_Website/blob/main/balanced_project/betteretf/helpers/asyncYahooSearch.py)

This module defines updates [YahooQuery](https://yahooquery.dpguthrie.com)'s Search function to except a list of search tearms and to search Yahoo Finance asynchronously.

`search(names)`

- returns: `list`
- Argument: `list` of string fund names (e.g. `['Vanguard S&P 500 ETF', 'iShare S&P Total Market Mutual Fund', etc.]`)


The first function, _get_fund(params), takes a dictionary of parameters and returns a JSON object containing information about a financial fund. The second function, get_funds(names), takes a list of fund names, creates a set of _get_fund functions with corresponding parameters, and uses asyncio.gather() to retrieve the data for all the funds asynchronously. Finally, the search(names) function simply calls get_funds() with the provided list of fund names using the asyncio.run() method and returns the resulting data as a list.


#### [betteretf.helpers.Matching](https://github.com/blakedaniel/Balanced_Website/blob/main/balanced_project/betteretf/helpers/matching.py)

This module matches user-defined criteria to fund objects. The matcher class takes a Fund object, which contains information about a particular ETF, and initializes several filters for matching. The matching criteria include holdings, beta, and expense ratio. The match function applies these filters to a list of ETFs and returns the top cap matching funds. The holdings_match function filters for funds that have similar holdings to the user's fund, while beta_match filters for funds that have a beta within 5% of the user's fund. The exp_ratio_match function filters for funds that have a lower expense ratio than the user's fund. The sectors_match function is not yet implemented. The matching function returns a list of ETFs that match the user's criteria, sorted by expense ratio. The number of matches is limited to the cap parameter.

# thank you to...
- Doug Guthrie and his [YahooQuery Library](https://yahooquery.dpguthrie.com)
