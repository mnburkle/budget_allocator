import json
import sys
from datetime import datetime
import argparse

MIN_DOLLARS_PER_CATEGORY = 2.50
BUDGET_CATEGORY_DECAY_RATE = 0.9

MONTHS = ["","January","February","March","April","May","June","July","August","September","October","November","December","January"]

def print_budget(budg, options=(0,0)):
    (use_savings_scheme, current_month_covered) = options
    total_budgeted = 0
    month_to_use_for_necessities =  datetime.today().month+1 if (not use_savings_scheme and current_month_covered) else datetime.today().month
    print("\n")
    for spending_type in budg:
        if(spending_type == "necessities"):
            print("------ " + spending_type.upper() + " (" + MONTHS[month_to_use_for_necessities] + ") ------" )
        else:
            print("------ " + spending_type.upper() + " (" + MONTHS[datetime.today().month] + ") ------" )

        for category in budg[spending_type]:
            if(len(category) < 10):
                print("    " + str(category) + ": \t\t" + str(budg[spending_type][category]))
            else:
                print("    " + str(category) + ": \t" + str(budg[spending_type][category]))

            total_budgeted += budg[spending_type][category]

    print("\nSum: " + str(total_budgeted))


def allocate_salary(total, options=(0,0)):
    (use_savings_scheme, _) = options


    with open("example_budgets.json") as f:
        budgets = json.load(f)
    if(use_savings_scheme):
        budget_to_use = budgets["savings_only_proportions"]
    else:
        budget_to_use = budgets["nominal_proportions"]

    # first we go through and look for numbers greater than 1, because
    # that implies that we have a set amount of money that we need to allocate.
    total_budgeted = 0
    for spending_type in budget_to_use:
        for category in budget_to_use[spending_type]:
            if(budget_to_use[spending_type][category] < 1):
                budget_to_use[spending_type][category] = budget_to_use[spending_type][category]*total
            total_budgeted += budget_to_use[spending_type][category]

    print(f"\nAllocating salary of ${args.t}...\nFinished first allocation based on json proportions and absolute requirements...\nBudgeted: ${total_budgeted}")
    overbudgeted_handling_option = 4
    attempts = 1
    while(total_budgeted > (total+1) and overbudgeted_handling_option > 0):
        while(overbudgeted_handling_option > 3):
            print("\nOverbudgeted :(!")
            overbudgeted_handling_option = input("Scale down everything (1), non-necessities (2), \n   discretionary only (3), or none (0)? ")
            try:
                overbudgeted_handling_option = int(overbudgeted_handling_option)
            except:
                print("Must be an integer! Preferably 0, 1, 2, or 3")
                overbudgeted_handling_option = 4

        max_dollars_per_category = 0
        total_budgeted = 0
        # LINEARLY SCALE ALL CATEGORIES BESIDES RENT
        if(overbudgeted_handling_option == 1):
            print(f"    scaling down everything (besides rent) by {BUDGET_CATEGORY_DECAY_RATE}, attempt #{attempts}")
            for spending_type in budget_to_use:
                for category in budget_to_use[spending_type]:
                    if(category != "rent"):
                        budget_to_use[spending_type][category] = budget_to_use[spending_type][category]*BUDGET_CATEGORY_DECAY_RATE
                        max_dollars_per_category = budget_to_use[spending_type][category] if budget_to_use[spending_type][category] > max_dollars_per_category else max_dollars_per_category
                    total_budgeted += budget_to_use[spending_type][category]
            attempts += 1

        # LINEARLY SCALE ALL NON NECESSITIES
        elif(overbudgeted_handling_option == 2):
            for spending_type in budget_to_use:
                for category in budget_to_use[spending_type]:
                    if(spending_type != "necessities"):
                        budget_to_use[spending_type][category] = budget_to_use[spending_type][category]*BUDGET_CATEGORY_DECAY_RATE
                        max_dollars_per_category = budget_to_use[spending_type][category] if budget_to_use[spending_type][category] > max_dollars_per_category else max_dollars_per_category
                    total_budgeted += budget_to_use[spending_type][category]
        # LINEARLY SCALE ALL DISCRETIONARY (fun savings + discretionary)
        elif(overbudgeted_handling_option == 3):
            for spending_type in budget_to_use:
                for category in budget_to_use[spending_type]:
                    if(spending_type == "discretionary" or (spending_type == "savings" and category == "fun savings")):
                        budget_to_use[spending_type][category] = budget_to_use[spending_type][category]*BUDGET_CATEGORY_DECAY_RATE
                        max_dollars_per_category = budget_to_use[spending_type][category] if budget_to_use[spending_type][category] > max_dollars_per_category else max_dollars_per_category
                    total_budgeted += budget_to_use[spending_type][category]
        else:
            break

        if(max_dollars_per_category < MIN_DOLLARS_PER_CATEGORY):
            print(f"    tried scaling down with option {overbudgeted_handling_option}, still overbudgeted so going leaner...")
            overbudgeted_handling_option = overbudgeted_handling_option-1

    # print_budget(budget_to_use, use_savings_scheme, current_month_covered)
    return budget_to_use
    

def choose_budget_scheme():
    today = datetime.today()

    is_current_month_covered = query_yes_no("Are necessities covered for %s? " % MONTHS[today.month]);
    if(is_current_month_covered):
        current_month_covered = True # put necessities towards N+1 month
        is_next_month_covered = query_yes_no("Are necessities covered for %s? " % MONTHS[today.month + 1]);
        if(is_next_month_covered):
            use_savings_scheme = True # no necessities at all
        else:
            use_savings_scheme = False # need necessities
    else:
        use_savings_scheme = False # need necessities
        current_month_covered = False # put necessities towards N month

    return (use_savings_scheme, current_month_covered)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if __name__ == '__main__':
    print(f"\nthis is a budget allocation tool that uses a preplanned budget (json) and allocates funds. \n\nif you the script overbudgets (aka you don't have enough money for it to fully allocate everything), it will ask you to scale down with varying degrees of leanness up until just paying for rent and nothing else.\n")

    parser = argparse.ArgumentParser()
    parser.add_argument('--t', help='total amount to budget', type=float, required=True)
    parser.add_argument('--json', help='json file containing budget allocations', required=True)
    parser.add_argument('--advanced', help='advanced budgeting if necessities are already covered for the month, include considerations for next month', action='store_true')
    args = parser.parse_args()

    options = (0,0)
    if(args.advanced):
        options = choose_budget_scheme()
    budget = allocate_salary(args.t, options)
    print_budget(budget, options)

