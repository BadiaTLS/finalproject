import pandas as pd

# Create a DataFrame with some dummy data
data = {'Name': ['John', 'Jane', 'Bob'],
        'Age': [30, 25, 40],
        'Salary': [50000, 60000, 70000]}
df = pd.DataFrame(data)

# Create a Pandas Excel writer using openpyxl as the engine
writer = pd.ExcelWriter('dummy_data.xlsx', engine='openpyxl')

# Convert the DataFrame to an XlsxWriter Excel object
df.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file
writer.save()