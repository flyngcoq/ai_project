import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path)

# Look for '수입 총계', '지출 총계'
print("\n--- Summary Rows ---")
summary_df = df[df['Unnamed: 1'].str.contains('총계|잔액|수지', na=False)]
print(summary_df.to_string())

# Look for specific categories
print("\n--- Categories ---")
print(df.iloc[10:50, 1:4].to_string()) # Unnamed: 1 is category, Unnamed: 2 is Total, Unnamed: 3 is Average
