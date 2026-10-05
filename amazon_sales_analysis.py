"""
Amazon Sales Dataset - cleaning, visualization and insights
Dataset: https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset
Put amazon.csv next to this script (or change CSV_PATH).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "amazon.csv"
OUT_DIR = "figures"
os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

# ------------------------------------------------------------------
# 1. LOAD + INSPECT
# ------------------------------------------------------------------
df = pd.read_csv(CSV_PATH)
print("Shape:", df.shape)
print(df.dtypes, "\n")
print("Missing values:\n", df.isna().sum(), "\n")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate product_id:", df["product_id"].duplicated().sum(), "\n")

# ------------------------------------------------------------------
# 2. CLEANING
# ------------------------------------------------------------------
# 2a. Duplicates: drop exact duplicates, then keep one row per product_id
n0 = len(df)
df = df.drop_duplicates()
df = df.drop_duplicates(subset="product_id", keep="first")
print(f"Removed {n0 - len(df)} duplicate rows")

# 2b. Data types: prices, discount, rating, rating_count are text
for col in ["discounted_price", "actual_price"]:
    df[col] = (df[col].astype(str)
               .str.replace("₹", "", regex=False)
               .str.replace(",", "", regex=False)
               .str.strip())
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"].astype(str).str.replace("%", "", regex=False),
    errors="coerce")

# rating has a stray bad value (e.g. '|') -> becomes NaN
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating_count"] = pd.to_numeric(
    df["rating_count"].astype(str).str.replace(",", "", regex=False),
    errors="coerce")

# 2c. Missing values
print("Missing after type conversion:\n", df[["rating", "rating_count"]].isna().sum())
df["rating"] = df["rating"].fillna(df["rating"].median())
df["rating_count"] = df["rating_count"].fillna(0)
df = df.dropna(subset=["discounted_price", "actual_price"])

# 2d. Category: split "A|B|C" into main and sub category
cats = df["category"].str.split("|")
df["main_category"] = cats.str[0]
df["sub_category"] = cats.str[-1]

# 2e. Outliers: flag with IQR rule (kept, but flagged; use log scale in plots)
def iqr_flags(s):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

for col in ["discounted_price", "actual_price", "rating_count"]:
    df[f"{col}_outlier"] = iqr_flags(df[col])
    print(f"{col}: {df[f'{col}_outlier'].sum()} outliers (IQR rule)")

# Sanity: discounted price should not exceed actual price
bad = df["discounted_price"] > df["actual_price"]
print("Rows where discounted > actual:", bad.sum())
df = df[~bad]

df.to_csv("amazon_clean.csv", index=False)
print("\nClean shape:", df.shape)

# ------------------------------------------------------------------
# 3. VISUALIZATIONS (6)
# ------------------------------------------------------------------
# 1. Top main categories by product count
fig, ax = plt.subplots(figsize=(9, 5))
order = df["main_category"].value_counts().head(10)
sns.barplot(x=order.values, y=order.index, ax=ax, color="#2a6f97")
ax.set(title="Products per main category", xlabel="Number of products", ylabel="")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/1_category_counts.png", dpi=150); plt.close(fig)

# 2. Distribution of ratings
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df["rating"], bins=20, kde=True, ax=ax, color="#e07a1f")
ax.set(title="Rating distribution", xlabel="Rating")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/2_rating_distribution.png", dpi=150); plt.close(fig)

# 3. Discount percentage distribution
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df["discount_percentage"], bins=25, ax=ax, color="#52796f")
ax.set(title="Discount percentage distribution", xlabel="Discount (%)")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/3_discount_distribution.png", dpi=150); plt.close(fig)

# 4. Average discount by main category
fig, ax = plt.subplots(figsize=(9, 5))
# only categories with >= 10 products, so tiny categories don't distort the averages
big = df["main_category"].value_counts()
big = big[big >= 10].index
avg_disc = (df[df["main_category"].isin(big)]
            .groupby("main_category")["discount_percentage"].mean().sort_values())
avg_disc.plot.barh(ax=ax, color="#9b2226")
ax.set(title="Average discount by main category", xlabel="Average discount (%)", ylabel="")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/4_avg_discount_by_category.png", dpi=150); plt.close(fig)

# 5. Actual price vs discounted price (log scale handles outliers)
fig, ax = plt.subplots(figsize=(7, 6))
sns.scatterplot(data=df, x="actual_price", y="discounted_price",
                hue="main_category", alpha=0.6, ax=ax, legend=False)
ax.set(xscale="log", yscale="log", title="Actual vs discounted price (log scale)")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/5_price_scatter.png", dpi=150); plt.close(fig)

# 6. Correlation heatmap
fig, ax = plt.subplots(figsize=(7, 5))
num = df[["discounted_price", "actual_price", "discount_percentage",
          "rating", "rating_count"]]
sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation between numeric features")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/6_correlation_heatmap.png", dpi=150); plt.close(fig)

# Bonus: price outliers by category (boxplot)
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df[df["main_category"].isin(big)], x="main_category", y="discounted_price", ax=ax)
ax.set(yscale="log", title="Discounted price by category (log scale)", xlabel="")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
fig.tight_layout(); fig.savefig(f"{OUT_DIR}/7_price_boxplot.png", dpi=150); plt.close(fig)

# ------------------------------------------------------------------
# 4. INSIGHTS (numbers to quote in your short report)
# ------------------------------------------------------------------
top_cat = df["main_category"].value_counts().idxmax()
most_reviewed = df.loc[df["rating_count"].idxmax()]
corr = num.corr()

print("\n===== KEY INSIGHTS =====")
print(f"Products analysed: {len(df)}")
print(f"Largest category: {top_cat} ({df['main_category'].value_counts().max()} products)")
print(f"Median rating: {df['rating'].median():.2f}; share rated >= 4.0: {(df['rating'] >= 4).mean():.1%}")
print(f"Average discount: {df['discount_percentage'].mean():.1f}%")
print(f"Category with highest avg discount (>=10 products): {avg_disc.idxmax()} ({avg_disc.max():.1f}%)")
print(f"Median actual price: {df['actual_price'].median():,.0f}; median discounted: {df['discounted_price'].median():,.0f}")
print(f"Most reviewed product: {most_reviewed['product_name'][:60]}... ({int(most_reviewed['rating_count']):,} ratings)")
print(f"Corr(discount %, rating): {corr.loc['discount_percentage', 'rating']:.2f}")
print(f"Corr(rating_count, rating): {corr.loc['rating_count', 'rating']:.2f}")
