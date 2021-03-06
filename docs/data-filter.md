---
type: feature
---
# data filter
process [[dataframe]]

## 非空的数据行
```python
#返回指定单列中没有空值的数据行
df[pd.notnull(df[col])]
df[df[col].notnull()]
#指定多列
#返回指定多列/df全部列中满足任意一列没有空值的数据行
df[df[[cols]].notnull().any(axis=1)] 
df[pd.notnull(df[[cols]]).any(axis=1)]
#返回指定多列中/df全部列中满足所有列没有空值的数据行
df[df[[cols]].notnull().all(axis=1)] 
df[pd.notnull(df[[cols]]).all(axis=1)]
```

## 数据筛选
---
1. 想要筛选出 B列大于零 的行
    ```python
    df1 = df[df['B']>0]
    ```
2. 筛选出 B列中大于零 的行，同时只显示B列的数据
    ```python
    df2 = df['B'][df['B'] >0] 
    ```
3. 筛选出 B列大于零，同时C列小于零的行
    ```python
    df3 = df[(df['B']>0)&(df['C']<0)]  # 这里&符号可以实现多条件的筛选
    ```
4. 根据B、C两列来筛选数据，但最终只显示A、D两列的数据
    ```python
    df4 = df[['A', 'D']][(df['B']>0)&(df['C']<0)]  
    ```

[//begin]: # "Autogenerated link references for markdown compatibility"
[dataframe]: dataframe "dataframe"
[//end]: # "Autogenerated link references"