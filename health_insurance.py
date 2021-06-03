#!/usr/bin/env python

"""
# Health Insurance Comparison Calculator

Compares a list of health insurance plans to show how each performs as medical
bills increase.

Running the script (more arguments available, see --help):
    
    python health_insurance.py 10000 < plans.csv

Accepts as input a csv file in the following format:

    name,monthly_premium,deductible,copay,coinsurance,out_of_pocket_max,employer_hsa_contribution,employee_hsa_contribution
    "HSA 2000-20",400,2000,0,0.20,8000,100,0
    "HSA 3000-20",300,3000,0,0.20,10000,100,0

Full explanation of fields:

* name, a human-friendly label for the plan
* monthly_premium, the monthly cost to you for this health insurance plan
* deductible, the plan's deductible
* out_of_pocket_max, the plan's out of pocket maximum
* coinsurance, the percentage of coinsurance you pay after the deductible is met
* hsa_contribution, an employer contribution to an HSA with this plan
* copay, the copay per office visit
"""

import argparse
import csv
import sys
import matplotlib.pyplot as plt


def parse_float(s):
    if not s:
        return 0
    return float(s)


class Plan(object):
    @classmethod
    def from_csv(cls, line):
        return cls(
            name=line['name'],
            monthly_premium=parse_float(line['monthly_premium']),
            deductible=parse_float(line['deductible']),
            out_of_pocket_max=parse_float(line['out_of_pocket_max']),
            coinsurance=parse_float(line['coinsurance']),
            employer_hsa_contribution=parse_float(line['employer_hsa_contribution']),
            employee_hsa_contribution=parse_float(line['employee_hsa_contribution']),
            copay=parse_float(line['copay']),
        )

    def __init__(self, monthly_premium, deductible, out_of_pocket_max, coinsurance=0, employer_hsa_contribution=0, employee_hsa_contribution=0, copay=0, name=None):
        self.monthly_premium = monthly_premium
        self.deductible = deductible
        self.out_of_pocket_max = out_of_pocket_max
        self.coinsurance = coinsurance
        self.employer_hsa_contribution = employer_hsa_contribution
        self.employee_hsa_contribution = employee_hsa_contribution
        self.copay = copay

        self.name = name

    def get_premium(self, months):
        return self.monthly_premium * months

    def get_tax_savings(self, tax_bracket):
        # print(self.employee_hsa_contribution, tax_bracket, self.employee_hsa_contribution * tax_bracket)
        return self.employee_hsa_contribution * tax_bracket

    def get_expenses(self, total_expenses, visits=0):
        copays = visits * self.copay
        if (copays + total_expenses) < self.deductible:
            expenses = copays + total_expenses
        else:
            expenses = copays + self.deductible + (total_expenses - copays - self.deductible) * self.coinsurance
            if expenses > self.out_of_pocket_max:
                expenses = self.out_of_pocket_max
        return expenses

    def get_actual_cost(self, total_expenses, months=12, visits=0, tax_bracket=0):
        # print(self.name, self.get_premium(months), self.get_expenses(total_expenses, visits=visits), self.employer_hsa_contribution, self.employee_hsa_contribution, self.get_tax_savings(tax_bracket))
        return self.get_premium(months) + self.get_expenses(total_expenses, visits=visits) - self.employer_hsa_contribution - self.get_tax_savings(tax_bracket)

    def __call__(self, *args, **kwargs):
        return self.get_actual_cost(*args, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('medical_bills', type=int, help="total medical bills over the coverage period")
    parser.add_argument('--months', type=int, default=12, help="number of months in this plan's coverage period (usually 12)")
    parser.add_argument('--visits', type=int, default=0, help="expected number of office visits")
    parser.add_argument('--tax', type=float, default=0, help="expected highest marginal income tax rate (when making HSA contributions)")
    args = parser.parse_args()

    reader = csv.DictReader(sys.stdin)
    plans = [Plan.from_csv(line) for line in reader]

    for p in plans:
        plt.plot(
            range(args.medical_bills),
            [p(c, args.months, args.visits, args.tax) for c in range(args.medical_bills)],
            label=p.name
        )

    plt.title("Health Insurance Comparison")
    plt.xlabel("Medical Bills")
    plt.ylabel("You Pay")
    plt.legend()
    plt.show()
