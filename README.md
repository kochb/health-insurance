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
