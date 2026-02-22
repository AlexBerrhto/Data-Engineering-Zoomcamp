import pandas as pd
import pyarrow
from datetime import date

today = date.today()
data = {'Name': ['Alex'], 'Gender': ['Male']}

df = pd.DataFrame(data)

df['Date'] = today
print("Successfully created a Pandas DataFrame:")
print(df)

df.to_parquet(f"output_{today}.parquet")