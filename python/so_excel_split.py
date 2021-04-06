import pandas as pd
import psycopg2
import datacompy
import os  

file_path = r'C:\excel_split\split_file\ONLY Reorder SO 导入20210402.xlsx'
new_excel_path = r'C:\excel_split\new_so_spilit.xlsx'
 
df = pd.read_excel(file_path)
cols = list(df) 
other_cols = cols[0:12] 
size_cols = cols[12:] 
so_ids = df['so_id'].unique().tolist() 
for so_id in so_ids:
    so_df = df[df['so_id'] == so_id] 
    size_df = so_df[size_cols].dropna(axis=1,how='all')
    excel_sheet_df = pd.concat([so_df[other_cols],size_df],axis=1) 
    writer = pd.ExcelWriter(new_excel_path, mode='a', engine='openpyxl')  
    excel_sheet_df.to_excel(writer, sheet_name=so_id , index =False) 
    writer.save()
    writer.close() 
    print(so_id) 