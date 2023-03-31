import yahooquery as yq

class Fund():
    """
    class that represents a fund
    """
    def __init__(self, ticker, exp_ratio):
        """
        initialize the class
        """
        self.ticker = ticker
        self.exp_ratio = exp_ratio

voo = yq.Ticker('VOO')
voo = Fund(voo.symbols[0], voo.fund_profile['VOO']['feesExpensesInvestment']['annualReportExpenseRatio'])

chasx = yq.Ticker('CHASX')
chasx = Fund(chasx.symbols[0], chasx.fund_profile['CHASX']['feesExpensesInvestment']['annualReportExpenseRatio'])


class expRatioCost(object):
    """
    class that calculates the cost of expense ratio
    """
    def __init__(self, fund, start_date, end_date):
        """
        initialize the class
        """
        self.fund = fund
        self.start_date = start_date
        self.end_date = end_date

    def get_exp_ratio(self):
        """
        get the expense ratio of the fund
        """
        return self.fund.exp_ratio

    def get_exp_ratio_cost(self):
        """
        get the cost of the expense ratio
        """
        # get the expense ratio
        exp_ratio = self.get_exp_ratio()
        # get the total value of the fund
        total_value = self.fund.get_total_value(self.start_date, self.end_date)
        # calculate the cost of the expense ratio
        exp_ratio_cost = total_value * exp_ratio
        return exp_ratio_cost