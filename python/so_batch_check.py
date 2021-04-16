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

        check_cols = ['so_id','city_group','repeat_from','plm_id','color_code','color_name','size_code','size_name','order_qty']
        check_cols.extend(size_cols) 
        excel_df = df.loc[:, check_cols]
        so_ids = df['so_id'].unique().tolist()
        
        so_ids_str = "'" + "','".join('%s' %i for i in so_ids)  + "'"
        
        conn = psycopg2.connect(database="linezone", user="postgres", password="Reorder_back-end@bestseller", host="10.150.60.15", port="5432")
        cur = conn.cursor()
        sql = """
        select so_id,city_group,repeat_from,plm_id,color_code,color_name
        ,size_code,size_name,order_qty
        from rst.rst_so_sku_city_group_detail
        where so_id in ({})
        """.format(so_ids) 
        cur.execute(sql)
        rows = cur.fetchall() 
        conn.close()
        result_df = pd.DataFrame(rows) 
        result_df.columns = check_cols 
        #excel_df.loc[:,'Style'] = excel_df.loc[:,'Style'].apply(str)
        compare = datacompy.Compare(excel_df,result_df,join_columns=['so_id', 'plm_id','color_code','size_code','city_group'])
        print(filename , compare.matches()) # 最后判断是否相等，返回 bool 
        if compare.matches() == False:
            print(compare.report()) # 打印报告详情，返回 string