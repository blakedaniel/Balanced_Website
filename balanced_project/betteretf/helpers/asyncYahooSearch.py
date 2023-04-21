from yahooquery.misc import _init_session
import asyncio


def _make_request(
    url, response_field=None, country=None, method="get", params={}, data=None, **kwargs
):
    session = _init_session(**kwargs)
    r = getattr(session, method)(url, params=params, json=data)
    return asyncio.wrap_future(r)

url = 'https://query2.finance.yahoo.com/v1/finance/search'

# asynchronous approach
async def _get_fund(params):
    url = 'https://query2.finance.yahoo.com/v1/finance/search'
    data = await _make_request(url, params=params, asynchronous=True)
    data = data.json()
    try:
        data = data["quotes"][0]
        return data
    except (KeyError, IndexError):
        return data

async def get_funds(names):
    funcs = set()

    for name in names:
        params = {
            'q': name,
            'quotesCount': 1,
            'newsCount': 0,
            'enableFuzzyQuery': False,
            'quotesQueryId': 'tss_match_phrase_query',
            'multiQuoteQueryId': 'multi_quote_single_token_query',
            'newsQueryId': 'news_cie_vespa',
            'enableCb': True,
            'enableNavLinks': False,
            'enableEnhancedTrivialQuery': True
        }
        funcs.add(_get_fund(params))

    data = await asyncio.gather(*funcs)
    data = list(data)
    return data

def search(names):
    return asyncio.run(get_funds(names))