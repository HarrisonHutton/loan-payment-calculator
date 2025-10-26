from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import ceil, log

import json


class Loan:
    def __init__(
            self, 
            name: str,
            apr: float,
            original_principal: float,
            current_principal: float,
            accrued_interest: float):
        self.name = name
        self.apr = apr
        self.daily_interest_rate = self.apr / 365
        self.original_principal = original_principal
        self.current_principal = current_principal
        self.accrued_interest = accrued_interest

    def display_payoff_date(
            self,
            fixed_interval_days: int, 
            payment_amount: float) -> str:
        today = datetime.today().date()
        loan_payoff_date = self.get_loan_payoff_date(fixed_interval_days, payment_amount)
        timedelta_days = (loan_payoff_date - today).days
        years_from_now = timedelta_days // 365
        extra_months_from_now = relativedelta(loan_payoff_date, today + relativedelta(years=years_from_now)).months
        number_of_payments = self.get_payments_remaining(fixed_interval_days, payment_amount)
        return \
            f"Your loan will be paid off by {loan_payoff_date}, which is about {years_from_now} years and {extra_months_from_now} months from now.\nThere are {number_of_payments} payments remaining."

    def get_current_balance(self) -> float:
        return self.current_principal + self.accrued_interest

    def get_progress_percent(self) -> float:
        """
        Return the percentage amount that is paid off for the loan as a 
        fraction. 
        """
        paid = self.original_principal - self.get_current_balance()
        return paid / self.original_principal

    def get_payments_remaining(
            self, 
            fixed_interval_days: int, 
            payment_amount: float) -> int:
        r_period = (1 + self.daily_interest_rate) ** fixed_interval_days - 1
        if payment_amount <= r_period * self.get_current_balance():
            raise Exception(f"The loan will never be paid off when making payments of ${payment_amount:.2f} every {fixed_interval_days} days.")
        numerator = -log(1 - ((r_period * self.get_current_balance()) / payment_amount))
        denominator = log(1 + r_period)
        return ceil(numerator / denominator)

    def get_loan_payoff_date(
            self,
            fixed_interval_days: int,
            payment_amount: float) -> datetime:
        today = datetime.today()
        payments_remaining = \
            self.get_payments_remaining(fixed_interval_days, payment_amount)
        payoff_date = today + relativedelta(days=fixed_interval_days * payments_remaining)
        return payoff_date.date()


def get_loan_from_json(filename: str) -> Loan:
    with open(filename) as f:
        data = json.load(f)
        return Loan(
            data["name"],
            data["apr"],
            data["original_principal"],
            data["current_principal"],
            data["accrued_interest"],
        )