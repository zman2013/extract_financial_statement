import tabula
import pandas as pd
import os

root_dir = '/Users/zman/financial_statement/li/'
filename = '2021-q4.pdf'
dir = root_dir + filename.split(".")[0] + "/"
if os.path.exists(dir) == False:
    os.makedirs(dir)

dfs = tabula.read_pdf(root_dir+'2021-q4.pdf', pages='all', guess=False)


# 预处理报表
# 1. 删除标注的一列
# 2. 拆分数字一列为两列
def pre_process(df: pd.DataFrame):
    if df is None:
        return None
    list = df.columns.values.tolist()
    if len(list) == 3:
        df = df.drop(df.columns[1], axis=1)
    df.insert(2, 'Unamed: 2', 0)
    for index, line in df.iterrows():
        array = str(line[1]).split(' ')
        if len(array) == 2:
            df.iat[index, 1] = array[0]
            df.iat[index, 2] = array[1]
    df = df.fillna(0)
    return df

import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
def convert_number(df: pd.DataFrame):
    if df is None:
        return None
    for index, line in df.iterrows():
        if line[1] == '–':
            line[1] = 0
        if line[2] == '–':
            line[2] = 0
        try:
            if line[1].startswith("("):
                line[1] = -int(line[1].replace("(","").replace(")","").replace(",",""))
            df.iat[index, 1] = locale.iat(line[1])
        except:
            None
        try:
            if line[2].startswith("("):
                line[2] = -int(line[2].replace("(","").replace(")","").replace(",",""))
            df.iat[index, 2] = locale.iat(line[2])
        except:
            None
        

# 提取财务报表
income_df0 = None  
income_df1 = None
balance_df0 = None
balance_df1 = None
cashflow_df0 = None
cashflow_df1 = None
i = 0
for df in dfs:
    df.to_csv(dir+str(i)+'.csv')
    i = i + 1
    first_column_name = str(df.columns.values.tolist()[0])
    print( ':'+first_column_name+':' )
    if first_column_name == '未經審計簡明合併綜合虧損表':
        income_df0 = df
    elif first_column_name == '未經審計簡明合併綜合虧損表(續)':
        df = df.rename(columns={first_column_name: '未經審計簡明合併綜合虧損表'})
        income_df1 = df
    elif first_column_name == '未經審計簡明合併資產負債表':
        balance_df0 = df
    elif first_column_name == '未經審計簡明合併資產負債表(續)':
        df = df.rename(columns={first_column_name: '未經審計簡明合併資產負債表'})
        balance_df1 = df
    elif first_column_name == '未經審計簡明合併現金流量表':
        cashflow_df0 = df
    elif first_column_name == '未經審計簡明合併現金流量表(續)':
        df = df.rename(columns={first_column_name: '未經審計簡明合併現金流量表'})
        cashflow_df1 = df

print(income_df0)
print(income_df1)
print(balance_df0)
print(balance_df1)
print(cashflow_df0)
print(cashflow_df1)

# 预处理报表
income_df0 = pre_process(income_df0)
income_df1 = pre_process(income_df1)
balance_df0 = pre_process(balance_df0)
balance_df1 = pre_process(balance_df1)
cashflow_df0 = pre_process(cashflow_df0)
cashflow_df1 = pre_process(cashflow_df1)

# 将 (number) 转为负数
convert_number(income_df0)
convert_number(income_df1)
convert_number(balance_df0)
convert_number(balance_df1)
convert_number(cashflow_df0)
convert_number(cashflow_df1)

# 合并报表
income_df = income_df0.append(income_df1, ignore_index=True)
balance_df = balance_df0.append(balance_df1, ignore_index=True)
cashflow_df = cashflow_df0.append(cashflow_df1, ignore_index=True)

# 输出到文件
income_df.to_csv(dir+'income_df.csv', index=False)
balance_df.to_csv(dir+'balance_df.csv', index=False)
cashflow_df.to_csv(dir+'cashflow_df.csv', index=False)
