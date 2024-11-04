# Project Buildup History: Local Business Profit Planning

- Repository: `local-business-profit-planning`
- Category: `product_case_study`
- Subtype: `analysis`
- Source: `project_buildup_2021_2025_daily_plan_extra.csv`
## 2024-09-16 - Day 3: Revenue modeling

- Task summary: Worked on the revenue modeling section of the Local Business Profit Planning case study today. Built a monthly revenue projection model that accounts for seasonality, growth assumptions, and customer churn. The model takes base revenue and a small number of assumptions as inputs and outputs a 12-month projection with confidence intervals. Made the assumption parameters easy to adjust so the tool can be used interactively.
- Deliverable: Revenue projection model with confidence intervals built. Assumptions parameterized for easy adjustment.
## 2024-09-16 - Day 3: Revenue modeling

- Task summary: The confidence interval calculation was using normal distribution symmetry which is not right for revenue (can't go below zero). Switched to a log-normal model for the lower bound.
- Deliverable: Revenue confidence intervals corrected with log-normal lower bound.
## 2024-09-23 - Day 4: Cost structure analysis

- Task summary: Did the cost structure analysis for the Local Business Profit Planning case study. Broke down fixed and variable costs, identified which cost categories scaled with revenue and which were step-function changes at certain business volumes. The biggest insight was that the payroll cost had a step change at the point where a second shift was needed — that inflection point defined a key capacity constraint in the planning model.
- Deliverable: Fixed vs variable cost breakdown done. Payroll step-function inflection point identified.
## 2024-11-04 - Day 5: Break-even analysis

- Task summary: Added a break-even analysis to the Local Business Profit Planning case study. Computed break-even revenue for each cost scenario and plotted the margin waterfall chart showing how each cost category reduces profit from gross revenue to net. The waterfall chart made the cost structure much more intuitive than the table version had been. Also computed payback period for the capital investment assumption.
- Deliverable: Break-even and payback period analysis added. Margin waterfall chart created.
## 2024-11-04 - Day 5: Break-even analysis

- Task summary: The waterfall chart logic had an off-by-one error in the cumulative sum calculation — fixed it and the totals now match the individual bars.
- Deliverable: Waterfall chart cumulative sum error fixed.
