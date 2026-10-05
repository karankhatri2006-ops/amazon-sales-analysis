# Amazon Sales Data Analysis

Data cleaning, exploratory analysis and visualization of the Amazon Sales Dataset using Python.

## Project Definition
This project cleans and analyzes Amazon product listings to understand pricing, discounts, ratings and customer reviews across product categories. It covers the full workflow: loading raw data, cleaning (missing values, duplicates, data types, outliers), creating visualizations, and summarizing insights.

## Dataset
- **Source:** [Amazon Sales Dataset on Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)
- **Content:** about 1,400 Amazon product listings with product ID and name, category, discounted price, actual price, discount percentage, rating, rating count, and review details.
- **Use case:** pricing and discount analysis, customer satisfaction, category comparison, and data-quality practice.

Download `amazon.csv` from Kaggle and place it in the project folder (or in `data/` and update `CSV_PATH` in the script).

## Data Cleaning Steps
1. **Duplicates:** removed exact duplicate rows and repeated `product_id`s.
2. **Data types:** converted price columns (removed ₹ and commas), `discount_percentage` (removed %), `rating` and `rating_count` to numeric.
3. **Missing values:** filled missing `rating` with the median and missing `rating_count` with 0.
4. **Feature engineering:** split `category` into `main_category` and `sub_category`.
5. **Outliers:** flagged with the IQR rule and kept in the data; log scales are used in plots.
6. **Validation:** removed rows where the discounted price exceeded the actual price.

## Visualizations
Saved in `figures/`:
1. Products per main category (bar chart)
2. Rating distribution (histogram)
3. Discount percentage distribution (histogram)
4. Average discount by category (bar chart)
5. Actual vs discounted price, log scale (scatter plot)
6. Correlation heatmap
7. Price by category (boxplot, extra)

## Tools and Libraries
Python 3, pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook / VS Code, Git and GitHub.

## How to Run
```bash
git clone https://github.com/<your-username>/amazon-sales-analysis.git
cd amazon-sales-analysis
pip install -r requirements.txt
python amazon_sales_analysis.py
```

## Repository Structure
```
amazon-sales-analysis/
├── README.md
├── requirements.txt
├── amazon_sales_analysis.py
├── amazon.csv              # raw data (download from Kaggle)
├── amazon_clean.csv        # generated cleaned data
├── figures/                # generated charts
└── insights_report.md      # short insights report
```

## Key Insights
- 1,465 rows cleaned to **1,351 unique products** (114 repeated product IDs removed).
- Electronics, Home&Kitchen and Computers&Accessories make up about 97% of products.
- Median rating is 4.1; 74.8% of products are rated 4.0 or higher.
- Average discount is 46.7%; Computers&Accessories discounts most (53.2%) among categories with 10+ products.
- Discount % has a weak negative correlation with rating (-0.16), so heavy discounts do not mean better ratings.

Full details: [insights_report.md](insights_report.md).
