import pandas as pd
import psycopg2
import datacompy
import os 

excel_path = r'C:\check'

for filepath,dirnames,filenames in os.walk(excel_path):
    for filename in filenames: 
        file_path = excel_path + '\\' + filename
        print(file_path)
        df = pd.read_excel(file_path)
 
        check_cols = ['Allocation Plan ID','PO ID','Style','Color Code','DC Code','Org Code','Plan Shop Date','Size Code','Manual Qty']  
        excel_df = df[check_cols]
        excel_df = excel_df[excel_df['Manual Qty']>0]
        allocation_ids = df['Allocation Plan ID'].unique().tolist() 
        allocation_ids_str = "'" + "','".join('%s' %i for i in allocation_ids)  + "'" 
        conn = psycopg2.connect(database="linezone", user="postgres", password="Reorder_back-end@bestseller", host="10.150.60.15", port="5432")
        cur = conn.cursor()
        sql = """
        select alloc_plan_id,po_id,product_code,color_code,dc_id,store_code,put_on_date,cast(size_code as int) size_code,sum(manual_alloc_qty) manual_alloc_qty
          from rst.rst_allocation_result 
        where alloc_plan_id in ({})
          and manual_alloc_qty > 0
        group by  alloc_plan_id,po_id,product_code,color_code,dc_id,store_code,put_on_date,size_code
        """.format(allocation_ids_str) 
        cur.execute(sql)
        rows = cur.fetchall() 
        conn.close()
        result_df = pd.DataFrame(rows) 
        result_df.columns = check_cols  
        excel_df['Style'] = excel_df['Style'].astype('str') 
        result_df['Style'] = result_df['Style'].astype('str') 
        compare = datacompy.Compare(excel_df,result_df,join_columns=['Allocation Plan ID','PO ID','Style','Color Code','DC Code','Org Code','Plan Shop Date','Size Code'])
        print(filename , compare.matches()) # 最后判断是否相等，返回 bool 
        if compare.matches() == False:
            print(compare.report()) # 打印报告详情，返回 string