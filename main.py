"""
This file demonstrates a use of the Loan class, where one wants to know how
long it would take to pay off an example loan, when making $1000 payments
every 14 days.
"""

from loan import get_loan_from_json


BIWEEKLY_PAYMENT_INTERVAL = 14  # 14 days between loan payments
BIWEEKLY_PAYMENT = 900


private_loan = get_loan_from_json("loan.example.json")

print(private_loan.display_payoff_date(BIWEEKLY_PAYMENT_INTERVAL, BIWEEKLY_PAYMENT))
