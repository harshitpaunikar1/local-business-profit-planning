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
