import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Re-evaluated bike scores (rider + pillion POV)
# File: bike_scores_eval.py

bikes = [
    ("Hero Xtreme 200S 4V", 1.41, "Entry-level 150–200cc"),
    ("Bajaj Pulsar RS200", 1.84, "Entry-level 150–200cc"),
    ("Yamaha R15 V4", 1.86, "Entry-level 150–200cc"),
    ("Suzuki Gixxer SF 250", 2.07, "200-250cc Single"),
    ("Hero Karizma XMR", 2.00, "200-250cc Single"),
    ("TVS Apache RR 310", 2.78, "300-400cc Single"),
    ("BMW G 310 RR", 3.05, "300-400cc Single"),
    ("KTM RC 125", 1.90, "Entry-level 150–200cc"),
    ("KTM RC 200", 2.23, "Entry-level 150–200cc"),
    ("KTM RC 390", 3.23, "300-400cc Single"),
    ("Kawasaki Ninja 300", 3.43, "300–500cc twins"),
    ("Yamaha R3", 3.60, "300–500cc twins"),
    ("Aprilia RS 457", 4.20, "300–500cc twins"),
    ("Kawasaki Ninja 500", 5.29, "300–500cc twins"),
    ("Kawasaki Ninja 650", 7.27, "Mid-weight"),
    ("Kawasaki Ninja ZX-4R", 8.79, "Mid-weight"),
    ("Suzuki GSX-8R", 9.25, "Mid-weight"),
    ("Triumph Daytona 660", 9.72, "Mid-weight"),
    ("Honda CBR650R", 10.40, "Mid-weight"),
    ("Kawasaki Ninja ZX-10R", 17.36, "Superbikes"),
    ("Suzuki Hayabusa", 16.90, "Superbikes"),
    ("Triumph Speed Triple 1200 RS", 20.39, "Superbikes"),
    ("Ducati Panigale V2", 20.68, "Superbikes"),
    ("BMW S 1000 RR", 21.10, "Superbikes"),
    # non faired
    ("KTM Duke 125", 1.50, "Entry-level 125–200cc"),
    ("KTM Duke 200", 2.10, "Entry-level 125–200cc"),
    ("TVS Apache RTR 200 4V", 1.85, "Entry-level 150–200cc"),
    ("Hero Xpulse 200", 1.50, "Entry-level 150–200cc"),
    ("Bajaj Pulsar N250", 1.95, "Entry-level 150–250cc"),
    ("Yamaha FZS-FI V3", 1.25, "Entry-level 150–200cc"),
    ("Suzuki Gixxer 250", 2.10, "200-250cc Single"),
    ("Honda CB300R", 2.40, "300-400cc Single"),
    ("KTM Duke 390", 3.25, "300–400cc Single"),
    ("Bajaj Dominar 400", 2.80, "300–400cc Single"),
    ("BMW G 310 R", 3.05, "300-400cc Single"),
    ("Kawasaki Z500", 5.30, "300–500cc Twins"),
    ("Royal Enfield Interceptor 650", 3.50, "300–500cc Twins"),
    ("Royal Enfield Continental GT 650", 3.50, "300–500cc Twins"),
    ("Honda CB500F", 5.30, "300–500cc Twins"),
    ("Honda CB500X", 5.50, "300–500cc Twins"),
    ("Honda H'ness CB350", 2.20, "300-400cc Single"),
    ("Royal Enfield Hunter 350", 2.00, "300-400cc Single"),
    ("Royal Enfield Classic 350", 1.85, "300-400cc Single"),
    ("Kawasaki Z650", 7.10, "Mid-weight 600–800cc"),
    ("Honda CB650R", 8.50, "Mid-weight 600–800cc"),
    ("Yamaha MT-07", 7.80, "Mid-weight 600–800cc"),
    ("Yamaha R7 (naked variant)", 8.00, "Mid-weight 600–800cc"),
    ("KTM Duke 790", 9.20, "Mid-weight 600–800cc"),
    ("KTM Duke 890", 9.50, "Mid-weight 600–800cc"),
    ("Kawasaki Z900", 9.90, "Superbikes 900cc+"),
    ("Kawasaki Z1000", 11.00, "Superbikes 900cc+"),
    ("Yamaha MT-09", 10.50, "Superbikes 900cc+"),
    ("Yamaha MT-10", 17.50, "Superbikes 900cc+"),
    ("Honda CB1000R", 14.50, "Superbikes 900cc+"),
    ("Ducati Streetfighter V4", 21.00, "Superbikes 900cc+"),
]

# Re-evaluated scores (rider + pillion POV). All values on 1-10 scale.
scores = {
    "Hero Xtreme 200S 4V": [4.5, 7.0, 8.0, 5.5, 6.5, 4.0],
    "Bajaj Pulsar RS200": [5.5, 6.5, 7.5, 6.5, 5.5, 5.0],
    "Yamaha R15 V4": [4.0, 6.0, 8.0, 5.5, 4.0, 3.5],

    "Suzuki Gixxer SF 250": [6.0, 7.0, 7.0, 6.5, 6.5, 6.0],
    "Hero Karizma XMR": [5.5, 7.0, 6.5, 6.5, 6.0, 6.0],

    "TVS Apache RR 310": [6.5, 6.0, 6.5, 7.0, 5.5, 6.0],
    "BMW G 310 RR": [6.0, 6.5, 6.5, 6.5, 6.0, 6.0],

    "KTM RC 125": [3.5, 5.5, 7.0, 5.0, 5.0, 3.0],
    "KTM RC 200": [5.0, 5.5, 7.0, 6.0, 5.0, 4.5],
    "KTM RC 390": [7.5, 5.5, 6.5, 7.5, 4.5, 6.5],

    "Kawasaki Ninja 300": [6.5, 7.0, 7.0, 7.0, 6.0, 6.5],
    "Yamaha R3": [7.0, 7.0, 7.0, 7.5, 6.0, 7.5],
    "Aprilia RS 457": [8.0, 7.0, 6.5, 8.0, 5.5, 8.0],
    "Kawasaki Ninja 500": [7.5, 7.5, 7.5, 7.5, 6.5, 7.5],

    "Kawasaki Ninja 650": [8.0, 8.0, 7.5, 8.5, 7.0, 7.5],
    "Kawasaki Ninja ZX-4R": [8.5, 4.5, 6.0, 8.5, 4.5, 9.0],
    "Suzuki GSX-8R": [8.5, 8.0, 7.5, 8.5, 7.5, 8.5],
    "Triumph Daytona 660": [8.5, 6.0, 6.5, 8.5, 6.0, 8.5],
    "Honda CBR650R": [8.0, 7.0, 6.5, 8.0, 6.0, 7.5],

    "Kawasaki Ninja ZX-10R": [9.5, 4.0, 5.0, 9.0, 3.5, 8.5],
    "Suzuki Hayabusa": [9.0, 7.5, 6.5, 9.5, 6.5, 8.0],
    "Triumph Speed Triple 1200 RS": [9.0, 6.5, 6.0, 9.0, 5.5, 8.5],
    "Ducati Panigale V2": [9.0, 4.0, 5.5, 9.0, 3.5, 8.5],
    "BMW S 1000 RR": [9.5, 4.0, 5.0, 9.5, 3.5, 8.5],

    # Non-faired / naked
    "KTM Duke 125": [4.5, 7.0, 7.5, 5.5, 3.5, 5.0],
    "KTM Duke 200": [5.5, 6.5, 7.0, 6.0, 3.5, 6.0],
    "TVS Apache RTR 200 4V": [5.0, 6.5, 6.5, 6.0, 4.0, 5.5],
    "Hero Xpulse 200": [4.0, 7.5, 6.5, 5.5, 3.0, 4.5],
    "Bajaj Pulsar N250": [5.5, 7.0, 7.0, 6.0, 4.5, 5.5],
    "Yamaha FZS-FI V3": [4.5, 6.5, 7.0, 5.5, 4.5, 5.0],

    "Suzuki Gixxer 250": [6.0, 7.0, 7.0, 6.5, 5.0, 6.0],
    "Honda CB300R": [6.5, 7.0, 7.0, 6.5, 4.5, 6.0],
    "KTM Duke 390": [8.0, 6.5, 6.5, 7.5, 4.5, 8.0],
    "Bajaj Dominar 400": [7.0, 7.0, 6.5, 7.0, 5.0, 7.0],
    "BMW G 310 R": [6.0, 7.0, 6.5, 6.5, 4.5, 6.0],

    "Kawasaki Z500": [7.5, 7.0, 7.0, 7.5, 5.5, 7.5],
    "Royal Enfield Interceptor 650": [6.5, 7.5, 6.0, 7.0, 6.5, 6.5],
    "Royal Enfield Continental GT 650": [6.0, 7.0, 6.0, 6.5, 6.0, 6.0],
    "Honda CB500F": [7.5, 7.5, 6.5, 7.5, 6.0, 7.5],
    "Honda CB500X": [7.0, 8.0, 7.0, 7.5, 6.5, 7.0],
    "Honda H'ness CB350": [6.0, 7.5, 6.5, 6.5, 5.5, 6.0],
    "Royal Enfield Hunter 350": [5.5, 7.0, 6.5, 6.0, 6.0, 5.5],
    "Royal Enfield Classic 350": [5.5, 6.5, 6.0, 6.0, 6.5, 5.5],

    "Kawasaki Z650": [8.0, 7.5, 7.0, 8.0, 6.0, 8.0],
    "Honda CB650R": [7.5, 7.5, 7.0, 7.5, 5.5, 7.5],
    "Yamaha MT-07": [8.5, 7.5, 7.0, 8.0, 6.0, 8.5],
    "Yamaha R7 (naked variant)": [8.0, 7.0, 7.0, 7.5, 5.0, 8.0],
    "KTM Duke 790": [8.5, 7.0, 6.5, 8.0, 4.5, 8.5],
    "KTM Duke 890": [8.5, 7.0, 6.5, 8.0, 4.5, 8.5],

    "Kawasaki Z900": [9.0, 7.5, 6.5, 8.5, 4.5, 9.0],
    "Kawasaki Z1000": [9.0, 7.0, 6.0, 8.5, 4.0, 9.0],
    "Yamaha MT-09": [9.0, 7.0, 6.0, 8.5, 4.0, 9.0],
    "Yamaha MT-10": [9.5, 6.5, 5.5, 9.0, 4.0, 9.0],
    "Honda CB1000R": [9.0, 7.0, 6.0, 8.5, 4.0, 8.5],
    "Ducati Streetfighter V4": [9.5, 6.0, 5.5, 9.5, 3.5, 9.5],
}

metrics = [
    "Performance (10 Yrs)",  # relevance and flaunt when on street
    "Comfort (All Ages)",
    "City Commute",
    "Weekend Ride",
    "Pillion Ride",
    "Fun (10+ yrs)",  # thrill, not getting boring
]

# Notes:
# - Values re-evaluated only from Rider + Pillion point-of-view (no brand/type bias).
# - Important adjustments: improved RC 390 comfort to 5.5 (was too low), lowered RC 390 pillion to 4.5;
#   raised RS457 comfort to 7.0; lowered ZX-4R comfort to 4.5; corrected Duke 390 pillion to 4.5; adjusted
#   Daytona 660 comfort to 6.0; nudged large nakeds (Z900/MT-09 etc.) comfort up modestly.

# Build DataFrame
df = pd.DataFrame(bikes, columns=["Bike", "Price (₹ Lakh)", "Segment"])
for m in metrics:
    df[m] = np.nan

# Fill scores
for name, score_list in scores.items():
    for i, m in enumerate(metrics):
        df.loc[df["Bike"] == name, m] = score_list[i]

# Total score and averages
df["Total score"] = df[metrics].sum(axis=1)
df["Total (out of 10)"] = df["Total score"] / len(metrics)

# VFM score calculation
value_raw = df["Total score"] / df["Price (₹ Lakh)"]
df["VFM score"] = 10 * (value_raw / value_raw.max())

# Ensure numeric columns are rounded
num_cols = (
    ["Price (₹ Lakh)"] + metrics + ["Total score", "Total (out of 10)", "VFM score"]
)
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce").round(2)

# --------------------
# PRINTING ALL LISTS
# --------------------
print("Faired Bikes 1–10 lakh: Ratings & Scores")
print(df.to_string(index=False))
print("\n" + "=" * 60)

## 🏆 All Bikes by Total Score (Best to Worst)
total_sorted = df.sort_values(by="Total score", ascending=False)
print("\n🏆 ALL BIKES BY TOTAL SCORE:")
print("-" * 40)
for rank, (i, row) in enumerate(total_sorted.iterrows(), 1):
    print(
        f"{rank}. {row['Bike']} - {row['Total score']}/60 ({row['Total (out of 10)']}/10)"
    )

## 💰 All Bikes by Value for Money (Best to Worst)
vfm_sorted = df.sort_values(by="VFM score", ascending=False)
print("\n💰 ALL BIKES BY VALUE FOR MONEY:")
print("-" * 40)
for rank, (i, row) in enumerate(vfm_sorted.iterrows(), 1):
    print(
        f"{rank}. {row['Bike']} - VFM Score: {row['VFM score']}/10 (₹{row['Price (₹ Lakh)']} lakh)"
    )

## 👑 All Bikes by Average Rank (Best to Worst)
total_rank_df = df.sort_values(by="Total score", ascending=False).reset_index()
total_rank_df["total_rank"] = total_rank_df.index + 1
total_rank_df = total_rank_df[["Bike", "total_rank"]]

vfm_rank_df = df.sort_values(by="VFM score", ascending=False).reset_index()
vfm_rank_df["vfm_rank"] = vfm_rank_df.index + 1
vfm_rank_df = vfm_rank_df[["Bike", "vfm_rank"]]

combined_ranks = pd.merge(total_rank_df, vfm_rank_df, on="Bike")
combined_ranks["average_rank"] = (
    combined_ranks["total_rank"] + combined_ranks["vfm_rank"]
) / 2
average_rank_sorted = combined_ranks.sort_values(by="average_rank", ascending=True)

print("\n👑 ALL BIKES BY AVERAGE RANK:")
print("-" * 40)
for rank, (i, row) in enumerate(average_rank_sorted.iterrows(), 1):
    bike_details = df[df["Bike"] == row["Bike"]].iloc[0]
    print(
        f"{rank}. {bike_details['Bike']} - Total: {bike_details['Total (out of 10)']}/10, VFM: {bike_details['VFM score']}/10 (Avg Rank: {row['average_rank']})"
    )

# Save CSV
csv_path = "faired_bikes_ratings_india_1to10L_aug2025.csv"
df.to_csv(csv_path, index=False)
print(f"\n📊 Data saved to: {csv_path}")

# --------------------
# VISUALIZATION
# --------------------
print("\n📈 Creating visualization...")

# Calculate All-rounder Score (100 - average rank)
average_rank_sorted["all_rounder_score"] = 100 - average_rank_sorted["average_rank"]

# Merge with bike details
plot_data = pd.merge(average_rank_sorted, df[["Bike", "Price (₹ Lakh)"]], on="Bike")

# Create scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(
    plot_data["Price (₹ Lakh)"],
    plot_data["all_rounder_score"],
    alpha=0.7,
    s=100,
    c="steelblue",
    edgecolors="black",
    linewidth=0.5,
)

# Add bike names as labels
for i, row in plot_data.iterrows():
    plt.annotate(
        row["Bike"],
        (row["Price (₹ Lakh)"], row["all_rounder_score"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8,
        alpha=0.8,
        rotation=15,
    )

plt.xlabel("Price (₹ Lakh)", fontsize=12, fontweight="bold")
plt.ylabel("All-rounder Score (100 - Average Rank)", fontsize=12, fontweight="bold")
plt.title(
    "Motorcycle Value Analysis: Price vs All-rounder Performance",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("bike_value_analysis.png", dpi=300, bbox_inches="tight")
plt.show()

print("📊 Graph saved as: bike_value_analysis.png")
