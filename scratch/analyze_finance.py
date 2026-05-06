import pandas as pd
import os

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"

try:
    df = pd.read_excel(file_path)
    
    print("--- Basic Info ---")
    print(df.info())
    
    print("\n--- First 20 Rows ---")
    print(df.head(20).to_string())
    
    # Try to identify columns for Income, Expense
    # Since column names are Unnamed in the summary, let's look at the first row (headers)
    print("\n--- Columns ---")
    print(df.columns.tolist())
    
    # Check if there's a row that looks like headers
    print("\n--- First Row Data ---")
    print(df.iloc[0].to_list())

except Exception as e:
    print(f"Error: {e}")
