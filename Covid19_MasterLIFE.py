import pandas as pd

sheet_id = "1roxOi2_Uw4YBzLd5s8vC8cp6lbuM9016tWeWTcx2q5Y"

oxygen_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=266242322"
df_oxygen = pd.read_csv(oxygen_url, usecols=["Name","Number", "Verified ", "Availability "])
new_df_oxygen = df_oxygen.dropna()
print(f"{new_df_oxygen.to_dict()}")
