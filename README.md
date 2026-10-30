# Atlas Global Retail: Why Is Profit Flat While Sales Boom? (Power BI)

**Analyst:** [Nuelwumi2024](https://github.com/Nuelwumi2024) · **Tools:** Power BI, DAX, Power Query, Python

> **Disclaimer:** *Atlas Global Retail* is a fictional company and all data is synthetic (seeded and reproducible with `src/generate_data.py`). This is a portfolio case study, not a real engagement.

> **Status:** complete. The finished report is [`report/Atlas_Sales_Profit_Analysis.pbix`](report/Atlas_Sales_Profit_Analysis.pbix) (open in Power BI Desktop on Windows). Data, DAX, theme and a rebuild guide are included.

![Power BI](https://img.shields.io/badge/Power%20BI-DAX%20%7C%20Power%20Query-F2C811?logo=powerbi&logoColor=black) ![Python](https://img.shields.io/badge/Python-data%20generation-3776AB?logo=python&logoColor=white) ![Data](https://img.shields.io/badge/Data-synthetic-2A9D8F)

**Contents:** [Summary](#executive-summary) · [Scenario](#1-the-scenario) · [The story](#the-story-chapter-by-chapter) · [Questions](#2-business-questions) · [Data model](#3-data-model) · [Metrics](#4-metrics-what-each-kpi-means-and-how-it-is-calculated) · [Build guide](#5-build-guide) · [Findings](#6-what-the-data-shows-verify-against-your-build) · [Recommendations](#7-recommendations) · [Challenges](#challenges-i-solved) · [Skills](#8-skills-demonstrated)

---

## Executive Summary

**The question:** Atlas Global Retail grew sales 43% in four years but profit only 6%. Where did the money go?

**The answer:** it did not disappear in one place. It leaked through **discounting**. Average discounts crept from 10.8% to 14.5%, and the 15.8% of order lines discounted 30% or more sold $505.5K of goods at a **$104.9K loss**. Two furniture lines (Tables and Bookcases), two weak markets (EMEA and LATAM) and costly premium shipping made it worse.

**The proof it is a margin problem, not a sales problem:** sales are within about 1% of target, but profit is **$488.8K against a $579.3K target (84%)**.

**The fix:** cap discounts at 20% and reprice the loss-making furniture. Holding sales volume constant, a 20% cap alone would have added about **$125K of profit (+26%)**, enough to close the profit gap to target.

---

## 1. The Scenario

**Atlas Global Retail** sells technology, furniture and office supplies to consumers, corporates and home offices in five markets: US, Canada, EMEA, APAC and LATAM.

It is November 2026. I have just joined as **Commercial Data Analyst**, and the 2027 budget is due in six weeks. In my first week the COO shows me one slide (January to October each year, so the comparison is like for like):

| Jan-Oct | 2023 | 2026 | Change |
|---|---|---|---|
| Sales | $0.76M | $1.09M | **+43%** |
| Profit | $98K | $104K | **+6%** |
| Profit margin | 12.9% | 9.6% | **-3.3 pts** |

> *"We're selling more every year and making almost no extra money. Where is the profit going, and what do we do about it before the 2027 budget is set?"*

The brief is to find out, and to hand the COO something she can act on. I had **9,818 order lines** covering 1 January 2023 to 28 October 2026, across customers, products, returns and annual targets.

---

## The Story, Chapter by Chapter

I built a four-page report and structured it like an investigation: first confirm the problem, then find where it sits, then find the cause, then check the smaller leaks.

### Chapter 1: Is the problem real? (Executive Overview)

![Executive Overview](images/page1-executive-overview.png)

**What I did.** I loaded five tables into Power BI, cleaned them in Power Query, modelled them as a star schema and wrote the core measures in DAX: sales, profit, margin, orders, customers, AOV and units. I added target measures that match each market's budget to the selected year, and a gauge comparing profit with its target.

**What I found.** The business is healthy on the surface: **$4.5M of sales, about 6K orders, 1K customers and a $800 average order**. Monthly sales climb with clear Q4 peaks, but the margin line drifts from the mid-teens in 2023 towards 10%. Sales are within about 1% of target in every market, while **profit sits at 84% of target** ($488.8K against $579.3K).

**So what.** The COO is right, and the problem is specific: Atlas is hitting its sales numbers and missing its profit numbers. Selling harder will not fix it, so I stopped asking *how much* we sell and started asking *what we make on it*.

### Chapter 2: Where does the profit come from and where does it go? (Products and markets)

![Where Profit Is Made and Lost](images/page2-where-profit-is-made-and-lost.png)

**What I did.** I compared profit and margin across categories, sub-categories, markets and countries, and built a Market × Category matrix to cut both at once.

**What I found.**
- **Technology earns the money** ($314K of profit, led by Copiers, Phones and Computers). **Office Supplies is the most efficient** (22.8% margin) but small.
- **Furniture is the problem child:** $1.5M of sales at only a **2.6% margin**. Tables and Bookcases are loss-making, even though they are among the biggest sellers.
- **The matrix tells the sharper story:** Furniture loses money in **EMEA (-3.5%) and LATAM (-2.0%)**. Canada is the strongest market in every category (17.8% overall), while **EMEA (5.1%) and LATAM (6.0%)** are the weakest, even though EMEA is a $0.93M market.

**So what.** Volume is hiding the damage. The products and regions that look busiest are among the least profitable, which pointed me towards pricing.

### Chapter 3: Why? (Discount damage)

![Discount Damage](images/page3-discount-damage.png)

**What I did.** I banded every order line by discount (none, low, medium, high), measured margin in each band, tracked the average discount by year, and isolated lines discounted 30% or more with their own sales, profit and loss share.

**What I found.** This is where the profit goes.
- **Margin collapses as discounts rise:** about 22% with no discount, 14% at low discounts, 3% at medium discounts, and **negative at high discounts**.
- **Discounts have crept up every year,** from 10.8% on average in 2023 to 14.5% in 2026.
- **Heavy discounts (30%+) generated $505.5K of sales and lost $104.9K.** About **14% of all order lines lose money.**
- **All ten Tables and Bookcases products are loss-making,** and Tables, one of the biggest sellers, sits at the bottom of the discount-versus-profit scatter with negative profit.

**So what.** This is the root cause. Atlas is buying growth with discounts, and the deepest discounts cost more than they bring in. It also explains why sales are on target while profit is not.

### Chapter 4: Are there other leaks? (Shipping and returns)

![Operations](images/page4-operations.png)

**What I did.** I compared margin by ship mode and analysed the 562 returned orders by reason.

**What I found.** The smaller leaks are real but secondary. **Same Day shipping earns about 6% margin against 12% for Standard Class**, so speed is being given away. Among returns, **"damaged in transit" is the top reason (32%)**, followed by "not as described" (23%), which points to packaging and carrier issues, not product quality. Average ship days move between about 3.9 and 4.7 days with no clear improvement.

**So what.** Shipping and returns are worth tidying up, but discounting is the big lever.

---

## Closing the Story: What I Would Tell the COO

> *"You do not have a sales problem. You have a pricing discipline problem. Sales are on target, but discounts have crept up every year, and the deepest ones lose money. Fix discounting first."*

| # | Decision for the 2027 budget | Evidence |
|---|---|---|
| 1 | **Cap discounts at 20%** and require approval above that | 30%+ lines lose $104.9K; capping at 20%, with volume held constant, would add about **$125K profit (+26%)** and close the profit gap to target |
| 2 | **Reprice or delist Tables and Bookcases** | Loss-making across all ten products |
| 3 | **Review EMEA and LATAM discounting** | 5-6% margins against 18% in Canada |
| 4 | **Charge for Same Day and First Class shipping** | Same Day earns half the margin of Standard |
| 5 | **Fix packaging and carrier issues** | Damage in transit drives 32% of returns |

**Honest caveats:** the $125K estimate holds sales volume constant (in reality some customers would buy less at a smaller discount), and the data is synthetic. In a real engagement I would test the cap on one market first and track the effect.

---

## 2. Business Questions

1. **Performance:** how are we doing against targets, and where are we falling short?
2. **Profitability:** which products, categories and markets make or lose money?
3. **Pricing:** are discounts driving growth, or destroying margin?
4. **Operations:** do shipping speed and returns eat into profit?

## 3. Data Model

Star schema with a fact table, three dimension-style tables, a targets table and a date table.

| Table | Rows | Role |
|---|---|---|
| `orders` | 9,818 | Fact: one row per order line (sales, profit, discount, shipping cost, quantity) |
| `customers` | 1,500 (1,261 have ordered) | Dimension: segment, market, region, country |
| `products` | 70 | Dimension: category, sub-category, product name |
| `returns` | 562 | One row per returned order, with the return reason |
| `targets` | 20 | Sales and profit targets per market and year (2026 is the year-to-date target) |
| `DateTable` / `Markets` | , | Calculated in DAX |

```
customers 1 ──< orders >── 1 products          Markets 1 ──< customers
DateTable 1 ──< orders                         returns linked to orders by OrderID
targets: no relationship, matched in the target measures with TREATAS
```

Every formula used in the report: [`dax/measures.dax`](dax/measures.dax).

## 4. Metrics (what each KPI means and how it is calculated)

| Metric | Definition | DAX idea |
|---|---|---|
| **Total Sales** | Revenue after discount | `SUM(Sales)` |
| **Total Profit** | Sales minus product cost and shipping cost | `SUM(Profit)` |
| **Profit Margin %** | Share of sales kept as profit | `Profit ÷ Sales` (never average the margin column) |
| **Orders** | Distinct orders (an order can have several lines) | `DISTINCTCOUNT(OrderID)` |
| **Customers** | Distinct buying customers | `DISTINCTCOUNT(CustomerID)` |
| **AOV** | Average order value | `Sales ÷ Orders` |
| **Units Sold** | Total quantity | `SUM(Quantity)` |
| **Sales Target / Profit Target** | Target for the selected year and market | `SUM(target)` with `TREATAS` on Year and Market |
| **Gauge Max** | Upper limit of the profit gauge (120% of target) | `Profit Target × 1.2` |
| **Avg Discount %** | Mean discount per order line | `AVERAGE(Discount)` |
| **Discount Band** | No / Low (up to 10%) / Medium (up to 20%) / High (over 20%) discount | `SWITCH(TRUE(), ...)` |
| **Heavy Discount Sales (30%+)** | Sales on lines discounted 30% or more | calculated column, summed |
| **Heavy Discount Profit** | Profit on lines discounted 30% or more | `CALCULATE(Profit, Discount>=0.3)` |
| **Loss-Making Share %** | Share of order lines with negative profit | `CALCULATE(COUNTROWS, Profit<0) ÷ COUNTROWS` |
| **Ship Days** | Days from order to dispatch | `DATEDIFF(OrderDate, ShipDate, DAY)` |
| **Returned orders** | Orders returned, by reason | `COUNT` of `returns[OrderID]` |

## 5. Build Guide

### Step 1: Load and clean (Power Query)
1. **Get Data → Text/CSV** and load all five CSVs from `data/`.
2. For `returns`, use **Use First Row as Headers** if the headers load as a data row.
3. In `orders`: set `OrderDate` and `ShipDate` to **Date**, and `Sales`, `Profit`, `Discount`, `ShippingCost` to **Decimal Number**.
4. Check the key columns in `customers` and `products` are text, then **Close & Apply**.

### Step 2: Model
1. Create `DateTable` and `Markets` (**New table**) from the first lines of `measures.dax`. Mark `DateTable` as a date table.
2. Add the relationships shown in section 3 (single direction, one-to-many). Leave `targets` unconnected.
3. Add the calculated columns, then the measures.
4. Import `theme/atlas-theme.json` via **View → Themes → Browse for themes**.

### Step 3: The four pages

| Page | Title | Story |
|---|---|---|
| 1 | **Executive Overview** | Growth is real, profit is not keeping up |
| 2 | **Where Profit Is Made and Lost** | Products and markets |
| 3 | **Discount Damage** | Pricing is the main leak |
| 4 | **Operations: Shipping & Returns** | Smaller leaks |

**Page 1: Executive Overview**
- **Cards:** Total Sales, Profit Margin %, Total Profit, Orders, Customers, AOV, Units Sold
- **Clustered column:** Sales Target and Total Sales by Market
- **Gauge:** Total Profit against Profit Target (Gauge Max as the maximum)
- **Combo chart:** Total Sales (columns) and Profit Margin % (line) by Year-Month
- **Slicers:** Year, Market, Segment

**Page 2: Where Profit Is Made and Lost**
- **Map:** Profit Margin % by Country
- **Bar chart:** Total Profit by Sub-Category
- **Matrix:** Market × Category, values = Profit Margin %
- **Treemap:** Total Sales by Category and Sub-Category, coloured by Profit Margin %

**Page 3: Discount Damage**
- **Cards:** Heavy Discount Sales (30%+), Heavy Discount Profit, Loss-Making Share %
- **Table:** Total Profit by product, filtered to the ten lowest
- **Line chart:** Avg Discount % by Year
- **Column chart:** Profit Margin % by Discount Band
- **Scatter:** Avg Discount % against Total Profit by Sub-Category, sized by Total Sales

**Page 4: Operations: Shipping & Returns**
- **Bar chart:** Profit Margin % by Ship Mode
- **Donut:** Returned orders by return reason
- **Line chart:** Average Ship Days by Year-Month

The report uses the custom theme and a consistent navy, teal and amber palette throughout.

## 6. What the Data Shows (verify against your build)

The data covers **1 January 2023 to 28 October 2026** (2026 is year to date), so use Jan-Oct comparisons or full years 2023-2025 when measuring growth.

- **Growth without profit:** comparing January-October each year, sales grew 43% between 2023 and 2026 while profit grew 6%, so margin fell from 12.9% to 9.6%.
- **Discounts are the main culprit.** Average discount rose from 10.8% in 2023 to 14.5% in 2026. Lines discounted 30% or more generated about **$506K of sales and a $105K loss**. Margin is about 22% with no discount, 14% at 10%, 3% at 20% and negative from 30%.
- **Furniture is the problem category:** $1.5M of sales but only about 3% margin. **Tables and Bookcases lose money** (about -$19K and -$5K) even though they are bestsellers.
- **Technology earns the most profit** ($314K), led by Copiers ($153K). **Office Supplies has the best margin** (about 23%) but small volume.
- **Markets differ sharply:** Canada has about 18% margin and the US about 14%. **EMEA** sells $0.93M at only about 5% margin, and **LATAM** about 6%. Both discount heavily.
- **Shipping:** Same Day earns about 6% margin and First Class 9%, against 12% for Standard Class.
- **Returns:** 562 orders were returned, and **damaged in transit is the top reason (32%)**, followed by not as described (23%).
- **Targets:** sales are within about 1% of target overall, but **profit is about 16% short** ($488.8K against $579.3K).

## 7. Recommendations

| Priority | Action | Why |
|---|---|---|
| 1 | **Cap discounts at 20%** and require approval above that | Lines at 30%+ lose money, and margin falls from about 22% to 3% between no discount and 20% off |
| 2 | **Reprice or delist Tables and Bookcases** | Loss-making at any meaningful discount |
| 3 | **Review EMEA and LATAM discount policy** | Large markets with 5-6% margin |
| 4 | **Charge for Same Day and First Class shipping** | Thin margins at these speeds |
| 5 | **Reduce damage in transit** (packaging, carrier review) | It is the top reason for returns (32% of returned orders) |

## Challenges I Solved

Real projects do not run cleanly. These are the problems I hit and how I fixed them.

| Problem | Cause | Fix |
|---|---|---|
| **Total Sales showed one $4.5M bar for every market** | The market table did not filter sales | Checked relationship direction and filtered through `customers[Market]` |
| **"Ambiguous paths" relationship error** | `targets` connected to the model by a second route, creating two paths to `orders` | Removed the extra relationship and matched targets in DAX with `TREATAS` on Year and Market |
| **Target bars were equal for every market** | A raw column was aggregated instead of a measure | Replaced it with a `Sales Target` measure |
| **Gauge showed "Count of ProfitTarget"** | The default aggregation on a numeric column was Count | Used the `Profit Target` measure, with a `Gauge Max` measure so the gauge scales sensibly |
| **Months plotted out of order** | Year-Month is text, so it sorted by value | Sorted the axis by Year-Month ascending |
| **Misleading numbers on cards (1K, 6K)** | Auto display units rounded values | Formatted measures as whole currency and set display units |

## 8. Skills Demonstrated

| Area | Evidence in this project |
|---|---|
| **Data modelling** | Star schema, one-to-many relationships, a calculated Markets table, resolving ambiguous relationship paths, `TREATAS` for budget data |
| **Power Query (ETL)** | Loading multiple sources, promoting headers, setting data types |
| **DAX** | Calculated tables and columns, `CALCULATE` with filters, `DIVIDE`, `DISTINCTCOUNT`, `SWITCH`, `DATEDIFF`, `TREATAS` |
| **Analytics** | Margin analysis, budget vs actual, discount impact, return analysis |
| **Visualisation** | Combo, treemap, scatter, matrix, gauge, map, donut, KPI cards |
| **Report design** | Custom theme, slicers, consistent layout and palette |
| **Business storytelling** | A clear question, findings, costed recommendations |

## 9. Repository

```
data/    orders, customers, products, returns, targets (synthetic CSVs)
dax/     measures.dax - every calculated table, column and measure used in the report
theme/   atlas-theme.json - custom Power BI theme
report/  Atlas_Sales_Profit_Analysis.pbix - the finished report
images/  dashboard screenshots (pages 1-4)
src/     generate_data.py - reproduces the data
```

```bash
pip install pandas numpy
python src/generate_data.py
```

## 10. About

Built by **[Nuelwumi2024](https://github.com/Nuelwumi2024)**. See also: [HR Attrition case study (Power BI)](https://github.com/Nuelwumi2024/powerbi-hr-attrition-dashboard).
