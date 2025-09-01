import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bikes = [
    # 125-200cc Segment
    ("Yamaha FZS-FI V3", 1.25, "125-200cc"),
    ("Hero Xtreme 200S 4V", 1.41, "125-200cc"),
    ("Hero Xpulse 200", 1.50, "125-200cc"),
    ("KTM Duke 125", 1.50, "125-200cc"),
    ("Bajaj Pulsar RS200", 1.84, "125-200cc"),
    ("TVS Apache RTR 200 4V", 1.85, "125-200cc"),
    ("Yamaha R15 V4", 1.86, "125-200cc"),
    ("KTM RC 125", 1.90, "125-200cc"),
    ("KTM Duke 200", 2.10, "125-200cc"),
    ("KTM RC 200", 2.23, "125-200cc"),
    # 201-400cc Segment
    ("Royal Enfield Classic 350", 1.85, "201-400cc"),
    ("Bajaj Pulsar N250", 1.95, "201-400cc"),
    ("Hero Karizma XMR", 2.00, "201-400cc"),
    ("Royal Enfield Hunter 350", 2.00, "201-400cc"),
    ("Suzuki Gixxer SF 250", 2.07, "201-400cc"),
    ("Suzuki Gixxer 250", 2.10, "201-400cc"),
    ("Honda H'ness CB350", 2.20, "201-400cc"),
    ("Honda CB300R", 2.40, "201-400cc"),
    ("TVS Apache RR 310", 2.78, "201-400cc"),
    ("Bajaj Dominar 400", 2.80, "201-400cc"),
    ("BMW G 310 RR", 3.05, "201-400cc"),
    ("BMW G 310 R", 3.05, "201-400cc"),
    ("KTM RC 390", 3.23, "201-400cc"),
    ("KTM Duke 390", 3.25, "201-400cc"),
    ("Kawasaki Ninja 300", 3.43, "201-400cc"),
    ("Yamaha R3", 3.60, "201-400cc"),
    ("Triumph Speed T4", 2.17, "201-400cc"),
    ("Triumph Speed 400", 2.35, "201-400cc"),
    ("Triumph Scrambler 400X", 2.65, "201-400cc"),
    ("Kawasaki Ninja ZX-4R", 8.79, "201-400cc"),
    # 401-600cc Segment
    ("Aprilia RS 457", 4.20, "401-600cc"),
    ("Kawasaki Ninja 500", 5.29, "401-600cc"),
    ("Honda CB500F", 5.30, "401-600cc"),
    ("Kawasaki Z500", 5.30, "401-600cc"),
    ("Honda CB500X", 5.50, "401-600cc"),
    # 601-800cc Segment
    ("Royal Enfield Interceptor 650", 3.50, "601-800cc"),
    ("Royal Enfield Continental GT 650", 3.50, "601-800cc"),
    ("Kawasaki Z650", 7.10, "601-800cc"),
    ("Kawasaki Ninja 650", 7.27, "601-800cc"),
    ("Yamaha MT-07", 7.80, "601-800cc"),
    ("Yamaha R7", 8.00, "601-800cc"),
    ("Honda CB650R", 8.50, "601-800cc"),
    ("KTM Duke 790", 9.20, "601-800cc"),
    ("Suzuki GSX-8R", 9.25, "601-800cc"),
    ("KTM Duke 890", 9.50, "601-800cc"),
    ("Triumph Daytona 660", 9.72, "601-800cc"),
    ("Honda CBR650R", 10.40, "601-800cc"),
    # 800cc+ Superbikes
    ("Kawasaki Z900", 9.90, "800cc+"),
    ("Yamaha MT-09", 10.50, "800cc+"),
    ("Kawasaki Z1000", 11.00, "800cc+"),
    ("Honda CB1000R", 14.50, "800cc+"),
    ("Suzuki Hayabusa", 16.90, "800cc+"),
    ("Kawasaki Ninja ZX-10R", 17.36, "800cc+"),
    ("Yamaha MT-10", 17.50, "800cc+"),
    ("Triumph Speed Triple 1200 RS", 20.39, "800cc+"),
    ("Ducati Panigale V2", 20.68, "800cc+"),
    ("Ducati Streetfighter V4", 21.00, "800cc+"),
    ("BMW S 1000 RR", 21.10, "800cc+"),
]

# Re-evaluated scores (rider + pillion POV). All values on 1-10 scale.
scores = {
    # 125-200cc Segment
    "Yamaha FZS-FI V3": [3.5, 6.5, 6.8, 4.0, 5.8, 4.0],
    "Hero Xtreme 200S 4V": [4.0, 6.2, 6.5, 4.2, 5.5, 4.2],
    "Hero Xpulse 200": [3.8, 5.5, 6.9, 4.0, 5.0, 3.8],
    "KTM Duke 125": [3.6, 4.5, 7.0, 4.0, 4.2, 3.5],
    "Bajaj Pulsar RS200": [4.2, 5.0, 6.3, 4.3, 4.8, 4.2],
    "TVS Apache RTR 200 4V": [4.3, 6.0, 6.5, 4.5, 5.5, 4.5],
    "Yamaha R15 V4": [4.0, 4.2, 6.0, 4.6, 4.0, 4.2],
    "KTM RC 125": [3.7, 3.8, 5.7, 4.2, 3.8, 3.7],
    "KTM Duke 200": [4.5, 5.0, 6.3, 4.4, 4.3, 4.5],
    "KTM RC 200": [4.6, 4.3, 6.0, 4.5, 4.0, 4.6],
    # 201-400cc Segment
    "Royal Enfield Classic 350": [4.0, 6.2, 5.0, 4.8, 6.5, 4.0],
    "Bajaj Pulsar N250": [4.5, 6.0, 6.0, 5.0, 5.0, 4.5],
    "Hero Karizma XMR": [4.7, 6.3, 5.5, 5.3, 6.0, 4.7],
    "Royal Enfield Hunter 350": [4.2, 6.0, 5.0, 4.8, 5.8, 4.2],
    "Suzuki Gixxer SF 250": [5.2, 5.0, 6.0, 5.5, 4.8, 5.2],
    "Suzuki Gixxer 250": [5.0, 6.0, 5.8, 5.4, 5.5, 5.0],
    "Honda H'ness CB350": [4.5, 6.5, 5.0, 5.2, 5.8, 4.5],
    "Honda CB300R": [4.6, 5.5, 5.8, 5.0, 4.0, 4.6],
    "TVS Apache RR 310": [5.2, 5.0, 5.5, 5.8, 4.2, 5.2],
    "Bajaj Dominar 400": [5.0, 6.2, 5.2, 5.7, 5.0, 5.0],
    "BMW G 310 RR": [4.8, 4.5, 5.0, 5.2, 4.0, 4.8],
    "BMW G 310 R": [4.9, 5.0, 5.2, 5.3, 4.2, 4.9],
    "KTM RC 390": [5.6, 4.0, 4.8, 6.0, 3.5, 5.6],
    "KTM Duke 390": [5.4, 5.0, 5.0, 6.2, 4.0, 5.4],
    "Kawasaki Ninja 300": [5.0, 4.5, 4.8, 5.5, 3.8, 5.0],
    "Yamaha R3": [5.2, 4.5, 4.5, 5.8, 4.0, 5.2],
    "Triumph Speed T4": [4.7, 6.0, 5.0, 5.5, 5.5, 4.7],
    "Triumph Speed 400": [4.8, 6.0, 5.2, 5.6, 5.5, 4.8],
    "Triumph Scrambler 400X": [5.0, 6.2, 5.0, 5.8, 5.5, 5.0],
    "Kawasaki Ninja ZX-4R": [5.8, 4.0, 4.5, 6.5, 4.0, 5.8],
    "Aprilia RS 457": [5.7, 4.5, 4.5, 6.2, 4.2, 5.7],
    # 401-600cc Segment
    "Kawasaki Ninja 500": [5.5, 5.0, 4.8, 6.0, 4.5, 5.5],
    "Honda CB500F": [5.2, 6.0, 5.0, 5.8, 5.5, 5.2],
    "Kawasaki Z500": [5.4, 6.0, 5.0, 6.0, 5.2, 5.4],
    "Honda CB500X": [5.0, 6.5, 4.8, 6.2, 5.8, 5.0],
    # 601-800cc Segment
    "Royal Enfield Interceptor 650": [5.2, 6.2, 4.8, 6.0, 5.5, 5.2],
    "Royal Enfield Continental GT 650": [5.0, 5.8, 4.5, 5.8, 5.0, 5.0],
    "Kawasaki Z650": [5.8, 6.5, 5.0, 6.2, 5.8, 5.8],
    "Kawasaki Ninja 650": [5.7, 5.8, 4.8, 6.0, 5.5, 5.7],
    "Yamaha MT-07": [6.0, 6.2, 5.0, 6.5, 6.0, 6.0],
    "Yamaha R7": [5.7, 5.5, 4.8, 6.0, 5.5, 5.7],
    "Honda CB650R": [5.5, 6.0, 4.8, 6.0, 5.8, 5.5],
    "KTM Duke 790": [6.2, 5.5, 4.8, 6.5, 5.2, 6.0],
    "Suzuki GSX-8R": [5.8, 6.0, 4.8, 6.2, 5.8, 5.8],
    "KTM Duke 890": [6.2, 5.8, 5.0, 6.5, 5.5, 6.2],
    "Triumph Daytona 660": [6.0, 5.5, 4.8, 6.2, 5.5, 6.0],
    "Honda CBR650R": [5.7, 5.8, 4.8, 6.0, 5.5, 5.7],
    # 800cc+ Superbikes
    "Kawasaki Z900": [7.0, 6.2, 4.5, 7.0, 6.0, 7.0],
    "Yamaha MT-09": [6.8, 5.5, 4.2, 6.8, 5.5, 6.8],
    "Kawasaki Z1000": [6.9, 5.8, 4.5, 7.0, 5.8, 6.9],
    "Honda CB1000R": [6.5, 6.0, 4.2, 6.8, 5.2, 6.5],
    "Suzuki Hayabusa": [7.0, 6.5, 4.5, 7.5, 6.5, 7.0],
    "Kawasaki Ninja ZX-10R": [8.0, 5.0, 4.5, 8.0, 5.0, 8.3],
    "Yamaha MT-10": [7.8, 6.2, 4.5, 7.8, 6.0, 7.8],
    "Triumph Speed Triple 1200 RS": [7.2, 5.5, 4.2, 7.2, 5.5, 7.2],
    "Ducati Panigale V2": [8.2, 5.0, 4.2, 7.8, 5.2, 8.6],
    "Ducati Streetfighter V4": [9.0, 5.5, 4.5, 9.0, 5.5, 10.0],
    "BMW S 1000 RR": [8.0, 5.2, 4.2, 8.5, 5.0, 8.5],
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
