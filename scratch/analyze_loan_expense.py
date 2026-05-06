import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path)

# Search for all rows that might contain loan-related expenditure details
keywords = ['대출', '이자', '상환', '금융', '원리금']

print("\n--- Detailed Loan & Finance Expenditure Search ---")
for index, row in df.iterrows():
    row_str = " ".join([str(val) for val in row.values if pd.notna(val)])
    if any(kw in row_str for kw in keywords):
        # Print the row if it seems to be in the 'Expenditure' context (likely rows 10-40)
        if 10 <= index <= 100:
            print(f"Row {index}: {row.iloc[1:16].to_list()}")

# Check if there's a separate section for 'Finance Details' further down
print("\n--- Rows 60-136 (Checking for detail sections) ---")
print(df.iloc[60:136, 1:6].to_string())
