import pandas as pd

df = pd.read_csv('European_Bank.csv')

# Engagement Classification
# - Active engaged customers (Active + >=2 products or Balance > 0? Let's keep it simple)
# Actually, the instructions say:
# Create engagement profiles:
# - Active engaged customers (IsActiveMember == 1, good balance/products)
# - Inactive disengaged customers (IsActiveMember == 0, low products/balance)
# - Active but low-product customers (IsActiveMember == 1, NumOfProducts == 1)
# - Inactive high-balance customers (IsActiveMember == 0, Balance > df.Balance.median())

median_bal = df[df['Balance'] > 0]['Balance'].median()

def classify_engagement(row):
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
        return 'Active Engaged'
    elif row['IsActiveMember'] == 0 and row['Balance'] > median_bal:
        return 'Inactive High-Balance'
    elif row['IsActiveMember'] == 1 and row['NumOfProducts'] == 1:
        return 'Active Low-Product'
    else:
        return 'Inactive Disengaged'

df['EngagementProfile'] = df.apply(classify_engagement, axis=1)

print("--- EDA Insights ---")
print("Churn by Engagement Profile:")
print(df.groupby('EngagementProfile')['Exited'].mean())

print("\nChurn by Num of Products:")
print(df.groupby('NumOfProducts')['Exited'].mean())

print("\nHigh-Balance Disengagement Rate:")
print(df[df['EngagementProfile'] == 'Inactive High-Balance']['Exited'].mean())

print("\nChurn by IsActiveMember:")
print(df.groupby('IsActiveMember')['Exited'].mean())
