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
        cols = list(df)
        i = 1
        size_cols = []

        for col in cols: 
            if col.find("Manual") >=0 :  
                new_col = "size_{}".format(i)
                df.rename(columns = {col:new_col},inplace=True)  
                size_cols.append(new_col) 
                i = i + 1   

        check_cols = ['PO ID','Style','Color Code','Org Code','Plan Shop Date']
        check_cols.extend(size_cols) 
        excel_df = df.loc[:, check_cols]
        style_ids = df['Style'].unique().tolist()
        color_ids = df['Color Code'].unique().tolist()
        style_ids_str = "'" + "','".join('%s' %i for i in style_ids)  + "'"
        color_ids_str = "'" + "','".join(color_ids)  + "'"
        conn = psycopg2.connect(database="linezone", user="postgres", password="Reorder_back-end@bestseller", host="10.150.60.15", port="5432")
        cur = conn.cursor()
        sql = """
        with size_n as (
        select product_code,color_code,size_code 
        ,row_number() over(partition by product_code,color_code order by size_code ) n
        from rst.rst_sku  
        where product_code in ({0}) and color_code in ({1})
        )
        select po_id, cast(a.product_code as VARCHAR) product_code,a.color_code,store_code,put_on_date 
        , sum(case when n = 1 then a.manual_alloc_qty end ) size_1
        , sum(case when n = 2 then a.manual_alloc_qty end ) size_2
        , sum(case when n = 3 then a.manual_alloc_qty end ) size_3
        , sum(case when n = 4 then a.manual_alloc_qty end ) size_4
        , sum(case when n = 5 then a.manual_alloc_qty end ) size_5
        , sum(case when n = 6 then a.manual_alloc_qty end ) size_6
        , sum(case when n = 7 then a.manual_alloc_qty end ) size_7
        , sum(case when n = 8 then a.manual_alloc_qty end ) size_8
        , sum(case when n = 9 then a.manual_alloc_qty end ) size_9 
        from rst.rst_allocation_result a 
        inner join size_n s on a.product_code=s.product_code and a.color_code = s.color_code and a.size_code = s.size_code
        where a.product_code in ({0}) and a.color_code in ({1})
        group by po_id,cast(a.product_code as VARCHAR),a.color_code,store_code,put_on_date 
        """.format(style_ids_str,color_ids_str) 
        cur.execute(sql)
        rows = cur.fetchall() 
        conn.close()
        result_df = pd.DataFrame(rows)
        result_df = result_df.loc[ 0: , 0:3+i]
        result_df.columns = check_cols
        excel_df = excel_df[excel_df[size_cols].notnull().any(axis=1)] 
        excel_df.loc[:,'Style'] = excel_df.loc[:,'Style'].apply(str)
        compare = datacompy.Compare(excel_df,result_df,join_columns=['PO ID', 'Style','Color Code','Org Code','Plan Shop Date'])
        print(filename , compare.matches()) # 最后判断是否相等，返回 bool 
        if compare.matches() == False:
            print(compare.report()) # 打印报告详情，返回 string