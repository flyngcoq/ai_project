import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
df = pd.read_excel(file_path)

# Look for the '금융' section and its sub-items
# In the previous run, '금융' was at index 19. Let's look at 19-50.
print("\n--- Detailed Finance & Expense Section ---")
print(df.iloc[10:60, 1:16].to_string())

# Search for keywords like '보험', '대출', '이자', '저축', '카드'
keywords = ['보험', '대출', '이자', '저축', '카드', '할부', '송금']
print("\n--- Keyword Search Results ---")
for kw in keywords:
    matches = df[df.astype(str).apply(lambda x: x.str.contains(kw, na=False)).any(axis=1)]
    if not matches.empty:
        print(f"\nKeyword '{kw}':")
        print(matches.iloc[:, 1:16].to_string())
