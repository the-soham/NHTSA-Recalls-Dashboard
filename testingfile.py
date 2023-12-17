import pandas as pd

df = pd.read_csv('Recalls_Data.csv')
print(df.columns)

df = df.drop(['NHTSA ID', 'Recall Link','Subject','Mfr Campaign Number','Recall Description','Do Not Drive Advisory','Park Outside Advisory ','Consequence Summary','Corrective Action','Completion Rate % (Blank - Not Reported)'], axis=1)
print(df.head())

#df = df.drop(['NHTSA ID', 'Recall Link','Subject','Mfr Campaign Number','Recall Description','Do Not Drive Advisory','Park Outside Advisory ','Consequence Summary','Corrective Action','Completion Rate % (Blank - Not Reported)'], axis=1)
df['Report Received Date'] = pd.to_datetime(df['Report Received Date'], format='%m/%d/%Y')
df['Year'] = df['Report Received Date'].dt.year

print(df.head())

recalls_by_manufacturer = df['Manufacturer'].value_counts().reset_index(name='Number of Recalls')
recalls_by_manufacturer = recalls_by_manufacturer.sort_values(by='Number of Recalls', ascending=False)

# Print the result
print(recalls_by_manufacturer)