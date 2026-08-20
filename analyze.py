# KEY FINDING: km_since_service is the dominant breakdown predictor (Cohen d = 1.06),
# followed by avg_daily_km (0.63) and load_factor (0.53). Total mileage and age show
# zero separation and do not predict breakdowns at all — older high-mileage cars are
# no more likely to fail than young low-mileage ones.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# --- Step 1: compare broke_down=0 vs broke_down=1 for every numeric column ---
nums = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("=== Group comparison (broke_down=0 vs 1) ===\n")
effects = {}
for col in nums:
    g0 = df[df["broke_down"] == 0][col]
    g1 = df[df["broke_down"] == 1][col]
    pooled_var = ((len(g0) - 1) * g0.std() ** 2 + (len(g1) - 1) * g1.std() ** 2) / (
        len(g0) + len(g1) - 2
    )
    d = (g1.mean() - g0.mean()) / pooled_var**0.5 if pooled_var > 0 else 0
    effects[col] = d
    tag = "STRONG" if abs(d) >= 0.8 else "MEDIUM" if abs(d) >= 0.5 else "WEAK" if abs(d) >= 0.2 else "NO"
    print(f"  {col:20s}  d={d:+.3f}  ({tag})")

# --- Step 2: pick columns with |d| >= 0.5 (medium or larger effect) ---
threshold = 0.5
predictors = [c for c, d in effects.items() if abs(d) >= threshold]
print(f"\nUsing predictors: {predictors}\n")

# --- Step 3: min-max normalise each predictor to 0-1, weight by |d|, sum to 0-100 ---
weights = {c: abs(effects[c]) for c in predictors}
total_weight = sum(weights.values())

risk = pd.Series(0.0, index=df.index)
for col in predictors:
    mn, mx = df[col].min(), df[col].max()
    normed = (df[col] - mn) / (mx - mn) if mx > mn else 0
    risk += normed * weights[col] / total_weight

df["risk_score"] = (risk * 100).round(1)

# --- Step 4: rank and print top 10 ---
ranked = df.sort_values("risk_score", ascending=False)
print("=== Top 10 highest-risk cars ===\n")
top10 = ranked.head(10)[["car_id", "km_since_service", "avg_daily_km", "load_factor", "risk_score", "broke_down"]]
print(top10.to_string(index=False))

# --- Step 5: quick validation — how well does the score separate the groups? ---
print("\n=== Validation ===\n")
broke = df[df["broke_down"] == 1]["risk_score"]
safe = df[df["broke_down"] == 0]["risk_score"]
print(f"  Broke-down cars: mean risk = {broke.mean():.1f}, median = {broke.median():.1f}")
print(f"  Safe cars:       mean risk = {safe.mean():.1f}, median = {safe.median():.1f}")
