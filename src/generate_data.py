"""Generates the synthetic 'Atlas Global Retail' dataset (star schema) for the Power BI report.

Run from the repo root:  python src/generate_data.py

Business patterns are deliberately built in so the dashboard has real stories to find:
  * Furniture (Tables, Bookcases) is loss-making once discounts pass its thin margin
  * Discounting is heavy in EMEA and LATAM, light in Canada
  * Same Day / First Class shipping eats margin
  * LATAM and Furniture have higher return rates
  * A small group of customers drives most of the sales
  * Sales grow every year, but profit grows more slowly (margin erosion)
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)

# --------------------------------------------------------------- products
sub = [  # category, sub-category, list price, base margin
    ("Technology", "Phones", 420, .32), ("Technology", "Computers", 900, .22),
    ("Technology", "Accessories", 60, .38), ("Technology", "Copiers", 1100, .28),
    ("Furniture", "Chairs", 310, .24), ("Furniture", "Tables", 520, .12),
    ("Furniture", "Bookcases", 380, .14), ("Furniture", "Furnishings", 70, .36),
    ("Office Supplies", "Binders", 18, .44), ("Office Supplies", "Paper", 12, .48),
    ("Office Supplies", "Storage", 85, .34), ("Office Supplies", "Appliances", 140, .30),
    ("Office Supplies", "Art", 22, .46), ("Office Supplies", "Labels", 9, .50),
]
prod_rows = []
for cat, sc, price, m in sub:
    for k in range(1, 6):
        prod_rows.append((f"P-{len(prod_rows)+1:03d}", f"{sc} {k:02d}", cat, sc,
                          round(price * rng.uniform(.8, 1.25), 2), m))
products = pd.DataFrame(prod_rows, columns=["ProductID", "ProductName", "Category", "SubCategory",
                                            "ListPrice", "BaseMargin"])

# --------------------------------------------------------------- geography / customers
geo = {  # market -> (region, [countries], discount profile, return rate multiplier)
    "US": ("North America", ["United States"], [.55, .2, .15, .07, .03], 1.0),
    "Canada": ("North America", ["Canada"], [.75, .15, .07, .03, 0], .8),
    "EMEA": ("Europe & Africa", ["United Kingdom", "Germany", "France", "Nigeria", "South Africa",
                                 "Egypt", "Spain"], [.30, .25, .20, .15, .10], 1.1),
    "APAC": ("Asia Pacific", ["Australia", "India", "China", "Japan", "Singapore"],
             [.45, .25, .15, .10, .05], 1.0),
    "LATAM": ("Latin America", ["Brazil", "Mexico", "Argentina", "Colombia"],
              [.28, .24, .22, .16, .10], 1.8),
}
market_w = {"US": .30, "Canada": .07, "EMEA": .27, "APAC": .24, "LATAM": .12}
disc_levels = [0, .1, .2, .3, .5]
segments = ["Consumer", "Corporate", "Home Office"]
first = ["Ade", "Chioma", "Liam", "Sofia", "Wei", "Priya", "Carlos", "Amara", "Noah", "Mei",
         "Omar", "Elena", "Kofi", "Hana", "Lucas", "Zara", "Ivan", "Nia", "Tariq", "Isla"]
last = ["Okafor", "Smith", "Garcia", "Chen", "Patel", "Silva", "Mensah", "Kim", "Rossi", "Ali",
        "Novak", "Dubois", "Sato", "Haddad", "Mueller", "Lopez", "Bello", "Nguyen", "Cohen", "Reyes"]
NC = 1500
cust_market = rng.choice(list(market_w), NC, p=list(market_w.values()))
customers = pd.DataFrame({
    "CustomerID": [f"C-{i:04d}" for i in range(1, NC + 1)],
    "CustomerName": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(NC)],
    "Segment": rng.choice(segments, NC, p=[.52, .30, .18]),
    "Market": cust_market,
})
customers["Region"] = customers.Market.map(lambda m: geo[m][0])
customers["Country"] = [rng.choice(geo[m][1]) for m in customers.Market]
customers["JoinYear"] = rng.choice([2022, 2023, 2024, 2025, 2026], NC, p=[.2, .27, .25, .2, .08])
cust_weight = rng.pareto(1.4, NC) + 1          # heavy tail: few customers buy a lot
cust_weight /= cust_weight.sum()

# --------------------------------------------------------------- orders
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
ship_days = {"Standard Class": (4, 7), "Second Class": (2, 5), "First Class": (1, 3), "Same Day": (0, 1)}
ship_cost_pct = {"Standard Class": .02, "Second Class": .03, "First Class": .055, "Same Day": .10}
priorities = ["Low", "Medium", "High", "Critical"]
year_w = {2023: .19, 2024: .24, 2025: .29, 2026: .28}      # growing business; 2026 is year-to-date
NO = 6200
years = rng.choice(list(year_w), NO, p=list(year_w.values()))
doy = rng.integers(0, 365, NO)
odate = pd.to_datetime(years.astype(str) + "-01-01") + pd.to_timedelta(doy, unit="D")
# Q4 seasonality: thin out Jan-Feb, keep Nov-Dec
keep = np.where(odate.month.isin([1, 2]), rng.random(NO) < .7, True)
odate = odate[keep & (odate <= pd.Timestamp('2026-10-28'))]   # data runs to the end of Oct 2026
NO = len(odate)
ocust = rng.choice(NC, NO, p=cust_weight)
orders = pd.DataFrame({
    "OrderID": [f"AG-{d.year}-{i:05d}" for i, d in enumerate(odate, 1)],
    "OrderDate": odate,
    "CustomerID": customers.CustomerID.values[ocust],
})
mkt = customers.Market.values[ocust]
ship = rng.choice(ship_modes, NO, p=[.58, .20, .15, .07])
orders["ShipMode"] = ship
orders["ShipDate"] = orders.OrderDate + pd.to_timedelta(
    [rng.integers(ship_days[s][0], ship_days[s][1] + 1) for s in ship], unit="D")
orders["OrderPriority"] = rng.choice(priorities, NO, p=[.25, .4, .25, .1])
orders = orders.sort_values("OrderDate").reset_index(drop=True)
orders["OrderID"] = [f"AG-{d.year}-{i:05d}" for i, d in enumerate(orders.OrderDate, 1)]
orders_mkt = dict(zip(orders.CustomerID, customers.set_index("CustomerID").Market.reindex(orders.CustomerID)))

# --------------------------------------------------------------- order lines (fact)
lines = []
cmap = customers.set_index("CustomerID")
prod_arr = products.to_records(index=False)
cat_w = {"Technology": .22, "Furniture": .26, "Office Supplies": .52}
pw = np.array([cat_w[c] / (products.Category == c).sum() for c in products.Category])
pw /= pw.sum()
for o in orders.itertuples(index=False):
    market = cmap.at[o.CustomerID, "Market"]
    for _ in range(rng.choice([1, 2, 3, 4], p=[.5, .3, .15, .05])):
        p = prod_arr[rng.choice(len(prod_arr), p=pw)]
        qty = int(rng.integers(1, 7 if p.ListPrice < 100 else 4))
        dp = np.array(geo[market][2], dtype=float)
        creep = min(.05 * (o.OrderDate.year - 2023), dp[0] * .9)   # discount creep: margin erosion
        dp[0] -= creep; dp[2] += creep
        disc = rng.choice(disc_levels, p=dp)
        sales = round(qty * p.ListPrice * (1 - disc), 2)
        cost = qty * p.ListPrice * (1 - p.BaseMargin)
        shipping = round(sales * ship_cost_pct[o.ShipMode] * rng.uniform(.8, 1.2), 2)
        profit = round(sales - cost - shipping, 2)
        lines.append((o.OrderID, o.OrderDate, o.ShipDate, o.ShipMode, o.OrderPriority, o.CustomerID,
                      p.ProductID, qty, disc, sales, shipping, profit))
fact = pd.DataFrame(lines, columns=["OrderID", "OrderDate", "ShipDate", "ShipMode", "OrderPriority",
                                    "CustomerID", "ProductID", "Quantity", "Discount",
                                    "Sales", "ShippingCost", "Profit"])
fact.insert(0, "LineID", range(1, len(fact) + 1))

# --------------------------------------------------------------- returns (separate file: practise a merge)
ordcat = fact.merge(products[["ProductID", "Category"]], on="ProductID")
omkt = fact.merge(customers[["CustomerID", "Market"]], on="CustomerID")
ret_p = (.045 * omkt.Market.map(lambda m: geo[m][3]).values
         * np.where(ordcat.Category == "Furniture", 1.6, 1.0))
returned = fact.loc[rng.random(len(fact)) < ret_p, ["OrderID"]].drop_duplicates()
returned["ReturnReason"] = rng.choice(["Damaged in transit", "Not as described", "Changed mind",
                                       "Late delivery", "Wrong item"], len(returned),
                                      p=[.28, .24, .20, .16, .12])
returned["Returned"] = "Yes"

# --------------------------------------------------------------- targets (budget vs actual)
agg = fact.merge(customers[["CustomerID", "Market"]], on="CustomerID")
agg["Year"] = agg.OrderDate.dt.year
t = agg.groupby(["Year", "Market"], as_index=False)[["Sales", "Profit"]].sum()
t["SalesTarget"] = (t.Sales * rng.uniform(.92, 1.12, len(t))).round(-2)
t["ProfitTarget"] = (t.Profit * rng.uniform(1.0, 1.35, len(t))).round(-2)    # profit targets are ambitious
targets = t[["Year", "Market", "SalesTarget", "ProfitTarget"]]

# --------------------------------------------------------------- write
for df, f in [(fact, "orders"), (customers, "customers"), (products.drop(columns="BaseMargin"), "products"),
              (returned, "returns"), (targets, "targets")]:
    df.to_csv(f"data/{f}.csv", index=False)
print(f"{len(fact)} order lines, {fact.OrderID.nunique()} orders, {NC} customers, {len(products)} products")
print(f"Sales {fact.Sales.sum():,.0f}  Profit {fact.Profit.sum():,.0f}  Margin {fact.Profit.sum()/fact.Sales.sum():.1%}")
print(agg.groupby("Year")[["Sales", "Profit"]].sum().assign(M=lambda x: x.Profit / x.Sales).round(3))
