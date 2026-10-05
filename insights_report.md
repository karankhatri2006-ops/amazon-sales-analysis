# Insights Report: Amazon Sales Dataset

## Data Cleaning Summary
- **Starting size:** 1,465 rows, 16 columns.
- **Duplicates:** no exact duplicate rows, but 114 repeated `product_id`s were removed, leaving **1,351 unique products**.
- **Data types:** prices, discount %, rating and rating count were all stored as text (₹, commas, % signs) and were converted to numbers. One rating held an invalid value (`|`) and became missing.
- **Missing values:** 1 missing rating (filled with the median) and 2 missing rating counts (filled with 0).
- **Outliers (IQR rule):** 209 in discounted price, 185 in actual price, 130 in rating count. These are real products (e.g. 65-inch TVs, very popular cables), so they were kept and flagged, and log scales were used in the plots.
- **Validation:** no rows had a discounted price higher than the actual price.

## Key Findings

**1. The catalogue is dominated by three categories.** Electronics (490), Home&Kitchen (448) and Computers&Accessories (375) make up about 97% of products. The other six categories have 31 products or fewer. USB cables are the largest sub-category (161 products).

**2. Ratings are high and tightly clustered.** The median rating is 4.1 and 74.8% of products are rated 4.0 or higher. Only 41 products are rated below 3.5. Because almost everything sits between 3.9 and 4.3, rating alone does little to separate good products from average ones.

**3. Discounts are large.** The average discount is 46.7% and about half of all products are discounted by 50% or more. The median actual price is ₹1,795 against a median discounted price of ₹899.

**4. Discount depth differs by category.** Among categories with at least 10 products, Computers&Accessories discounts most (53.2% on average), then Electronics (49.9%) and Home&Kitchen (40.1%). OfficeProducts discounts least (12.4%) but has the highest average rating (4.31).

**5. Cheaper products are discounted more deeply.** Discount % has a weak negative correlation with discounted price (-0.24), so low-priced items such as cables carry the biggest percentage discounts.

**6. Discounts do not buy better ratings.** Discount % and rating are weakly negatively correlated (-0.16), and rating count and rating are only weakly positively correlated (0.10). Heavy discounting and popularity do not strongly predict quality ratings.

**7. A few products attract most of the reviews.** The most reviewed product (an AmazonBasics HDMI cable) has 426,973 ratings, far above the typical product, which explains the large number of rating-count outliers. The most expensive products are 65-inch 4K TVs (up to ₹77,990).

## Conclusion
The dataset is dominated by Electronics, Home&Kitchen and Computers&Accessories, with heavy discounting (about 47% on average) and uniformly high ratings. Price and discount are linked (cheaper items are discounted more), but ratings are largely independent of both discount and popularity. Analyses of this data should therefore focus on category and price patterns rather than expecting ratings to explain sales behaviour.

## Limitations
The dataset is a small sample of listings, has no sales volume or date column, and has very few products outside the three main categories, so conclusions about small categories are unreliable.
