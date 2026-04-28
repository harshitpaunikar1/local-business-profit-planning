"""
Profit planning tool for local businesses.
Models revenue, costs, break-even, and scenario analysis for small business financial planning.
"""
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


@dataclass
class RevenueStream:
    name: str
    units_per_month: float
    unit_price: float
    growth_rate_monthly: float = 0.0   # fraction, e.g. 0.02 for 2%
    seasonality: Optional[List[float]] = None  # 12-element multiplier list

    @property
    def monthly_revenue(self) -> float:
        return self.units_per_month * self.unit_price


@dataclass
class CostStructure:
    fixed_monthly: float          # rent, salaries, utilities
    cogs_pct: float               # cost of goods as % of revenue (0-1)
    variable_other_pct: float     # other variable costs as % of revenue
    depreciation_monthly: float = 0.0
    loan_payment_monthly: float = 0.0

    @property
    def total_fixed(self) -> float:
        return self.fixed_monthly + self.depreciation_monthly + self.loan_payment_monthly


class BreakEvenAnalyzer:
    """Computes break-even point in units and revenue for a business."""

    def __init__(self, fixed_costs: float, unit_price: float,
                 variable_cost_per_unit: float):
        self.fixed_costs = fixed_costs
        self.unit_price = unit_price
        self.variable_cost = variable_cost_per_unit

    @property
    def contribution_margin(self) -> float:
        return self.unit_price - self.variable_cost

    @property
    def contribution_margin_ratio(self) -> float:
        return self.contribution_margin / self.unit_price if self.unit_price > 0 else 0

    def break_even_units(self) -> float:
        return self.fixed_costs / self.contribution_margin if self.contribution_margin > 0 else float("inf")

    def break_even_revenue(self) -> float:
        return self.fixed_costs / self.contribution_margin_ratio if self.contribution_margin_ratio > 0 else float("inf")

    def margin_of_safety(self, actual_revenue: float) -> float:
        """Excess revenue above break-even as fraction of actual."""
        ber = self.break_even_revenue()
        return (actual_revenue - ber) / actual_revenue if actual_revenue > 0 else 0.0

    def operating_leverage(self, actual_units: float) -> float:
        """Degree of operating leverage at current output."""
        beu = self.break_even_units()
        if actual_units <= beu:
            return float("inf")
        return actual_units / (actual_units - beu)


class ProfitPlanner:
    """
    12-month profit planning model for a local business.
    Supports multiple revenue streams, cost structures, and what-if scenario analysis.
    """

    def __init__(self, revenue_streams: List[RevenueStream], cost_structure: CostStructure):
        self.revenue_streams = revenue_streams
        self.cost = cost_structure

    def _get_seasonality(self, stream: RevenueStream, month_idx: int) -> float:
        if stream.seasonality and len(stream.seasonality) == 12:
            return stream.seasonality[month_idx]
        return 1.0

    def monthly_forecast(self, months: int = 12) -> pd.DataFrame:
        """Generate month-by-month P&L forecast."""
        records = []
        running_units = {s.name: s.units_per_month for s in self.revenue_streams}
        for m in range(months):
            month_rev = 0.0
            for stream in self.revenue_streams:
                units = running_units[stream.name] * self._get_seasonality(stream, m % 12)
                rev = units * stream.unit_price
                month_rev += rev
                running_units[stream.name] *= (1 + stream.growth_rate_monthly)
            cogs = month_rev * self.cost.cogs_pct
            variable_other = month_rev * self.cost.variable_other_pct
            total_variable = cogs + variable_other
            gross_profit = month_rev - total_variable
            ebitda = gross_profit - self.cost.fixed_monthly
            ebit = ebitda - self.cost.depreciation_monthly
            net_profit = ebit - self.cost.loan_payment_monthly
            records.append({
                "month": m + 1,
                "revenue": round(month_rev, 2),
                "cogs": round(cogs, 2),
                "gross_profit": round(gross_profit, 2),
                "fixed_costs": round(self.cost.fixed_monthly, 2),
                "ebitda": round(ebitda, 2),
                "net_profit": round(net_profit, 2),
                "gross_margin_pct": round(gross_profit / month_rev * 100, 2) if month_rev > 0 else 0.0,
                "net_margin_pct": round(net_profit / month_rev * 100, 2) if month_rev > 0 else 0.0,
            })
        return pd.DataFrame(records)

    def scenario_analysis(self, scenarios: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare multiple scenarios (e.g. optimistic, base, pessimistic).
        Each scenario is a dict of parameter overrides.
        """
        results = []
        base_df = self.monthly_forecast()
        base_annual = {
            "scenario": "base",
            "annual_revenue": round(base_df["revenue"].sum(), 2),
            "annual_net_profit": round(base_df["net_profit"].sum(), 2),
            "months_profitable": int((base_df["net_profit"] > 0).sum()),
        }
        results.append(base_annual)
        for scenario_name, overrides in scenarios.items():
            price_mult = overrides.get("price_multiplier", 1.0)
            volume_mult = overrides.get("volume_multiplier", 1.0)
            cost_mult = overrides.get("cost_multiplier", 1.0)
            modified_streams = [
                RevenueStream(
                    name=s.name,
                    units_per_month=s.units_per_month * volume_mult,
                    unit_price=s.unit_price * price_mult,
                    growth_rate_monthly=s.growth_rate_monthly,
                    seasonality=s.seasonality,
                )
                for s in self.revenue_streams
            ]
            modified_cost = CostStructure(
                fixed_monthly=self.cost.fixed_monthly * cost_mult,
                cogs_pct=self.cost.cogs_pct,
                variable_other_pct=self.cost.variable_other_pct,
                depreciation_monthly=self.cost.depreciation_monthly,
                loan_payment_monthly=self.cost.loan_payment_monthly,
            )
            planner = ProfitPlanner(modified_streams, modified_cost)
            df = planner.monthly_forecast()
            results.append({
                "scenario": scenario_name,
                "annual_revenue": round(df["revenue"].sum(), 2),
                "annual_net_profit": round(df["net_profit"].sum(), 2),
                "months_profitable": int((df["net_profit"] > 0).sum()),
            })
        return pd.DataFrame(results)

    def kpi_summary(self, df: Optional[pd.DataFrame] = None) -> Dict:
        if df is None:
            df = self.monthly_forecast()
        total_rev = df["revenue"].sum()
        total_net = df["net_profit"].sum()
        return {
            "annual_revenue": round(total_rev, 2),
            "annual_net_profit": round(total_net, 2),
            "avg_net_margin_pct": round(float(df["net_margin_pct"].mean()), 2),
            "months_profitable": int((df["net_profit"] > 0).sum()),
            "best_month": int(df.loc[df["net_profit"].idxmax(), "month"]),
            "worst_month": int(df.loc[df["net_profit"].idxmin(), "month"]),
        }


if __name__ == "__main__":
    np.random.seed(42)
    cafe_seasonality = [0.9, 0.9, 1.0, 1.1, 1.1, 1.2, 1.2, 1.1, 1.0, 0.95, 0.95, 1.1]
    streams = [
        RevenueStream("Dine-in", units_per_month=2000, unit_price=18.0,
                      growth_rate_monthly=0.01, seasonality=cafe_seasonality),
        RevenueStream("Takeout", units_per_month=800, unit_price=14.0,
                      growth_rate_monthly=0.02),
        RevenueStream("Catering", units_per_month=5, unit_price=1200.0,
                      growth_rate_monthly=0.005),
    ]
    cost = CostStructure(
        fixed_monthly=18000,
        cogs_pct=0.32,
        variable_other_pct=0.08,
        depreciation_monthly=500,
        loan_payment_monthly=1200,
    )
    planner = ProfitPlanner(revenue_streams=streams, cost_structure=cost)
    forecast = planner.monthly_forecast()
    print("12-Month P&L Forecast:")
    print(forecast[["month", "revenue", "gross_profit", "ebitda", "net_profit", "net_margin_pct"]].to_string(index=False))

    print("\nKPI Summary:", planner.kpi_summary(forecast))

    scenarios = {
        "optimistic": {"price_multiplier": 1.10, "volume_multiplier": 1.15, "cost_multiplier": 1.02},
        "pessimistic": {"price_multiplier": 0.92, "volume_multiplier": 0.85, "cost_multiplier": 1.05},
    }
    scenario_df = planner.scenario_analysis(scenarios)
    print("\nScenario Analysis:")
    print(scenario_df.to_string(index=False))

    be = BreakEvenAnalyzer(
        fixed_costs=cost.total_fixed,
        unit_price=18.0,
        variable_cost_per_unit=18.0 * (cost.cogs_pct + cost.variable_other_pct),
    )
    print(f"\nBreak-even units/month: {be.break_even_units():.0f}")
    print(f"Break-even revenue/month: ${be.break_even_revenue():,.0f}")
