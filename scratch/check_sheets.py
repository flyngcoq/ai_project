import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
xl = pd.ExcelFile(file_path)
print(f"Sheet names: {xl.sheet_names}")

for sheet in xl.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(f"\n--- Sheet: {sheet} (First 10 rows) ---")
    print(df.head(10).to_string())
