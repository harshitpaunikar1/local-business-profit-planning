# Local Business Profit Planning Diagrams

Generated on 2026-04-26T04:29:37Z from README narrative plus project blueprint requirements.

## Profitability by product/customer

```mermaid
flowchart TD
    N1["Step 1\nEngaged nearby organisations; mapped processes, objectives, constraints, decision "]
    N2["Step 2\nConsolidated ledgers, invoices, POS exports, surveys; cleaned and reconciled into "]
    N1 --> N2
    N3["Step 3\nAssessed seasonality and cohorts; quantified product/customer profitability and dr"]
    N2 --> N3
    N4["Step 4\nBuilt planning model for pricing, promotions, reorder levels with simple what-if s"]
    N3 --> N4
    N5["Step 5\nPresented insights via brief reports and dashboards; set weekly reviews, owner app"]
    N4 --> N5
```

## Seasonal demand patterns

```mermaid
flowchart LR
    N1["Inputs\nInbound API requests and job metadata"]
    N2["Decision Layer\nSeasonal demand patterns"]
    N1 --> N2
    N3["User Surface\nAPI-facing integration surface described in the README"]
    N2 --> N3
    N4["Business Outcome\nmeasurable KPI exports are not checked in, so only intended operational "]
    N3 --> N4
```

## Evidence Gap Map

```mermaid
flowchart LR
    N1["Present\nREADME, diagrams.md, local SVG assets"]
    N2["Missing\nSource code, screenshots, raw datasets"]
    N1 --> N2
    N3["Next Task\nReplace inferred notes with checked-in artifacts"]
    N2 --> N3
```
