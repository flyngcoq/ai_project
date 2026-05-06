import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path, sheet_name='가계부 내역')

# Filter for '금융' category
finance_tx = df[df['대분류'] == '금융']

print("\n--- Top 30 Finance Transactions (Largest Amounts) ---")
# Convert '금액' to positive for sorting if it's negative
finance_tx['abs_amount'] = finance_tx['금액'].abs()
print(finance_tx.sort_values(by='abs_amount', ascending=False).head(30).to_string())

# Group by '소분류' and '내용' to see where the money goes
print("\n--- Finance Summary by Sub-Category and Content ---")
summary = finance_tx.groupby(['소분류', '내용'])['금액'].sum()
print(summary.sort_values())
