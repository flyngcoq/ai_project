import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path)

# Look at the detailed rows in the Expenditure section (starting from row 17-18)
# We saw '금융' at row 19. Let's see if there are nested rows.
print("\n--- Rows around Finance (Index 19) ---")
print(df.iloc[15:40, 1:6].to_string())

# Search for the exact string '금융' and see if there are other occurrences
print("\n--- All '금융' Occurrences ---")
print(df[df['Unnamed: 1'] == '금융'].to_string())

# Check if there are rows with '카드' or '보험' in the same section
print("\n--- Card and Insurance in Expense Section ---")
print(df.iloc[17:35, 1:6].to_string())
