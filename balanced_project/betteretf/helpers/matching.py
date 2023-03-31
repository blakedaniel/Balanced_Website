from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown

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
        self.user_fund = user_fund
        self.user_holdings = user_fund.holdings.all()
        self.user_sectors = user_fund.sectors
        self.user_beta = user_fund.beta
        self.user_exp_ratio = user_fund.exp_ratio


    def beta_match(self, funds=Fund.objects.all()):
        """
        filter for funds with beta within 1% of user_fund.beta
        """
        return funds.filter(beta__gte=float(self.user_beta) * .99, beta__lte=float(self.user_beta) * 1.01)
    
    def exp_ratio_match(self, funds=Fund.objects.all()):
        """
        filter for funds with expense ratio less than user_fund.exp_ratio
        """
        return funds.filter(exp_ratio__lte=self.user_exp_ratio)
    
    def holdings_match(self, funds=Fund.objects.all()):
        """
        filter for funds with holdings within 75% of user_fund.holdings
        """
        user_fund_holdings = set([holding.holding_ticker for holding in self.user_holdings.all()])
        funds_holdings = []
        for fund in funds:
            fund_holdings = set([holding.holding_ticker for holding in fund.holdings.all()])
            if len(user_fund_holdings.intersection(fund_holdings)) / len(user_fund_holdings) > .75:
                funds_holdings.append(fund)
        return funds_holdings

    def sectors_match(self, funds=Fund.objects.all()):
        """
        filter for funds with sector holdings with 75% of sectors are within 75% of user_fund.sectors
        """
        pass

    def match(self, cap=10, funds=Fund.objects.all()):
        """
        return a list of funds that match user_fund
        """
        funds = funds.exclude(ticker=self.user_fund.ticker)
        matched_funds = self.beta_match(funds)
        matched_funds = self.exp_ratio_match(matched_funds)
        matched_funds = self.holdings_match(matched_funds)
        matched_funds.sort(key=lambda x: x.exp_ratio)

        # limit the number of funds returned
        cap = min(len(matched_funds) - 1, cap)
        matched_funds = matched_funds[:cap]
        return matched_funds
