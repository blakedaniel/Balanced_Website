from betteretf.models import Fund
from django.shortcuts import HttpResponse

# match a given user_fund object to funds in the database where...
# user_fund.beta * .99 < fund.beta < user_fund.beta * 1.01
# itersection of user_fund.holdings and fund.holdings > 75%
# itersection of user_fund.sectors and fund.sectors > 75%
# fund.exp_ratio < user_fund.exp_ratio

class matcher(object):
    def __init__(self, user_fund):
        """
        when initializing, user_fund is a Fund object
        """
        self.match_criteria_filter = set()
        self.user_fund = user_fund

        try:
            self.user_holdings = user_fund.holdings.all()
            if len(self.user_holdings) > 0:
                self.match_criteria_filter.add(self.holdings_match)
        except:
            HttpResponse(f'Error finding holdings for: {user_fund}')
        try:
            self.user_sectors = user_fund.sectors
        except:
            HttpResponse(f'Error finding sectors for: {user_fund}')
        try:
            self.user_beta = user_fund.beta
            self.match_criteria_filter.add(self.beta_match)
        except:
            HttpResponse(f'Error finding beta for: {user_fund}')
        try:
            self.user_exp_ratio = user_fund.exp_ratio
            self.match_criteria_filter.add(self.exp_ratio_match)
        except:
            HttpResponse(f'Error finding expense ratio for: {user_fund}')


    def beta_match(self, funds=Fund.objects.all()):
        """
        filter for funds with beta within 5% of user_fund.beta
        """
        return funds.filter(beta__gte=float(self.user_beta) * .95, beta__lte=float(self.user_beta) * 1.05)
    
    def exp_ratio_match(self, funds=Fund.objects.all()):
        """
        filter for funds with expense ratio less than user_fund.exp_ratio
        """
        return funds.filter(exp_ratio__lte=self.user_exp_ratio)
    
    def holdings_match(self, funds=Fund.objects.all()):
        # TODO: make sure that this is accurately filtering funds
        """
        filter for funds with holdings within 25% of user_fund.holdings
        """
        user_fund_holdings = set([holding.holding_ticker for holding in self.user_holdings.all()])
        funds_holdings = []
        for fund in funds:
            fund_holdings = set([holding.holding_ticker for holding in fund.holdings.all()])
            if len(user_fund_holdings.intersection(fund_holdings)) / len(user_fund_holdings) > .75:
                funds_holdings.append(fund)
        funds_holdings = Fund.objects.filter(ticker__in=[fund.ticker for fund in funds_holdings])
        return funds_holdings

    def sectors_match(self, funds=Fund.objects.all()):
        """
        filter for funds with sector holdings with 75% of sectors are within 75% of user_fund.sectors
        """
        pass

    def match(self, cap=3, funds=Fund.objects.all()):
        """
        return a list of funds that match user_fund
        """
        matched_funds = funds.exclude(ticker=self.user_fund.ticker)

        for filter in self.match_criteria_filter:
            matched_funds = filter(matched_funds)
        if matched_funds.exists():
            matched_funds = matched_funds.order_by('exp_ratio')

        # limit the number of funds returned
        cap = min(max(len(matched_funds) - 1, 0), cap)
        matched_funds = matched_funds[:cap]
        return matched_funds
