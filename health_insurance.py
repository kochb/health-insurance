#!/usr/bin/env python

"""
# Health Insurance Comparison Calculator

Compares a list of health insurance plans to show how each performs as medical
bills increase.

Running the script (more arguments available, see --help):
    
    python health_insurance.py 10000 < plans.csv

Accepts as input a csv file in the following format:

    name,monthly_premium,deductible,out_of_pocket_max,coinsurance,hsa_contribution,copay
    "HSA 2000-20",400,2000,8000,0.20,100,0
    "HSA 3000-20",300,3000,10000,0.20,100,0

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
            hsa_contribution=parse_float(line['hsa_contribution']),
            copay=parse_float(line['copay']),
        )

    @staticmethod
    def build_plan_function(monthly_premium, deductible, out_of_pocket_max, coinsurance=0, hsa_contribution=0, copay=0):
        def fn(total_expenses, months=12, visits=0):
            premium = monthly_premium * months

            copays = visits * copay
            if (copays + total_expenses) < deductible:
                expenses = copays + total_expenses
            else:
                expenses = copays + deductible + (total_expenses - copays - deductible) * coinsurance
                if expenses > out_of_pocket_max:
                    expenses = out_of_pocket_max

            return premium + expenses - hsa_contribution

        return fn

    def __init__(self, monthly_premium, deductible, out_of_pocket_max, coinsurance=0, hsa_contribution=0, copay=0, name=None):
        self.fn = self.build_plan_function(monthly_premium, deductible, out_of_pocket_max, coinsurance, hsa_contribution, copay)
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('medical_bills', type=int, help="total medical bills over the coverage period")
    parser.add_argument('--months', type=int, default=12, help="number of months in this plan's coverage period (usually 12)")
    parser.add_argument('--visits', type=int, default=0, help="expected number of office visits")
    args = parser.parse_args()

    reader = csv.DictReader(sys.stdin)
    plans = [Plan.from_csv(line) for line in reader]

    for p in plans:
        plt.plot(
            range(args.medical_bills),
            [p(c, args.months, args.visits) for c in range(args.medical_bills)],
            label=p.name
        )

    plt.title("Health Insurance Comparison")
    plt.xlabel("Medical Bills")
    plt.ylabel("You Pay")
    plt.legend()
    plt.show()
