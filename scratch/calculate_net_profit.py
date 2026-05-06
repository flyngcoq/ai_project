import pandas as pd

file_path = "/Users/flyngcoq/AI_Project/Obsidian_Vault/50_Resources/Attachments/20260505_234949_2025-05-05~2026-05-05.xlsx"
tx_df = pd.read_excel(file_path, sheet_name='가계부 내역')

# 1. Total Rental Income (사업수입)
income_df = tx_df[(tx_df['타입'] == '수입') & (tx_df['대분류'] == '사업수입')]
total_income = income_df['금액'].sum()

# 2. Total Plaza Loan Payments (Interest/Repayment)
# Based on previous analysis, these are '대출 4545981' and '대출 0777893'
plaza_loans = tx_df[tx_df['내용'].str.contains('대출 4545981|대출 0777893', na=False)]
total_loan_exp = plaza_loans['금액'].abs().sum()

# 3. Total Property Tax (재산세)
prop_tax = tx_df[tx_df['내용'].str.contains('재산세|김포|중구청', na=False) & (tx_df['소분류'] == '세금/과태료')]
total_prop_tax = prop_tax['금액'].abs().sum()

# 4. Total Income Tax (종소세)
income_tax = tx_df[tx_df['내용'].str.contains('국세_최연수|김포세무서', na=False)]
total_income_tax = income_tax['금액'].abs().sum()

print(f"Annual Rental Income: {total_income:,}")
print(f"Annual Plaza Loan Exp: {total_loan_exp:,}")
print(f"Annual Property Tax: {total_prop_tax:,}")
print(f"Annual Income Tax (Total): {total_income_tax:,}")

# Net Profit calculation (Assuming 50% of Income Tax is from Plaza)
net_annual = total_income - total_loan_exp - total_prop_tax - (total_income_tax * 0.5)
print(f"\nEstimated Net Annual Profit: {net_annual:,}")
print(f"Estimated Net Monthly Profit: {net_annual/12:,}")
