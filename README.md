# budget_allocator

This is a budget allocator tool I made for when I get a pay check. It uses a json file with some budgeting requirements, and then takes the total amount in the pay check and tries to put it towards the provided budget. If the paycheck isn't enough to satisfy the requirements within the budget, then there are options for scaling down, including cutting out descretionary spending, reducing savings, or even cutting down on necessities. 

usage: `python3 budget_allocator.py --t [total paycheck amount] --json [budget.json] [--advanced]`

## making your own budget JSON file

I've provided an example budget json, and it has two components (keys): `nominal_proportions`, and `savings_only_proportions`. The nominal budget describes your entire budget, made up of `necessities` like rent and food and gas, `savings` either for retirement or short term emergencies or even vacations, and `discretionary` which are just for fun. "Savings only" mode is usually for the case where all your necessities are covered, and you're looking to put your paycheck towards either your savings or discretionary spending only. If you're just using this tool for the first time, you can ignore this. 

Every field in the budget JSON can be either a proportion (p < 1.0), or an fixed value >= 1. I found this was the most flexible option to accommodate fixed costs like rent or internet, as well as more flexible categories like "savings" which are usually encouraged to be some percentage of your take-home pay. 

## how the budget allocation works

The budget allocator will first do a basic sum of all of your absolute fixed costs + (your provided total) x (all the proportions). So, it's to your benefit to make sure your budget's proportions sort of add up to 1.0, or add up to whatever percent of your paycheck you have left after rent (if you're in the Bay Area you can probably make all your proportions add up to like 0.30 haha... :(... yeah). But if you don't do that, it's fine, the tool will just have an overly ambitious initial budget allocation. 

If this initial budget is over the total provided, you have a few options for scaling down - you can either remove discretionary allocations only, remove savings allocations (and discretionary), or scale down everything until it fits. The tool will keep you updated as it tries to make everything work. Currently, if things get desperate and it can't cover even the necessities, the budget allocation tool will decay all your proportions + fixed costs by a factor of 0.9 each time it over budgets, except for specifically the "rent" key which is protected. This was helpful for me when I didn't have enough money for much more besides rent, and helped me figure out how to best divide the rest of my paycheck (#gradschool). 

It often happens that the final budget allocation doesn't QUITE add up to the total (a few dollars will be left here and there depending on how much the tool had to scale down your categories), but I've found it to be a good start to help think through the general distribution of my paycheck. Happy budgeting!
