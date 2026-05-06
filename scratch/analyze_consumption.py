import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path)

# Extract Consumption Categories (Index 17 to 32)
consumption_categories = df.iloc[17:33, 1:16]
print("\n--- Monthly Consumption (Excluding Finance) ---")
print(consumption_categories.to_string())

# Calculate averages for key categories
# Unnamed: 3 was the '월평균' (Monthly Average) column in some views, but let's check.
# Actually, the columns 2025-05 to 2026-05 are indices 4 to 16.

# Filter out '금융' (Index 19) to see 'Pure Consumption'
pure_consumption = df.iloc[[17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], 4:16].apply(pd.to_numeric, errors='coerce').sum()
print("\n--- Total Pure Consumption (Monthly) ---")
print(pure_consumption)

# Top Categories
category_sums = df.iloc[[17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], 1:16].set_index('Unnamed: 1')
category_totals = category_sums.iloc[:, 3:].apply(pd.to_numeric, errors='coerce').sum(axis=1)
print("\n--- Total Spending by Category (1 Year Sum) ---")
print(category_totals.sort_values(ascending=False))
