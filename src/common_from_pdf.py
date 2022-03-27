import tabula
import pandas as pd
import os

root_dir = '/Users/zman/financial_statement/tesla/'
filename = '2021-q4.pdf'
dir = root_dir + filename.split(".")[0] + "/"
if os.path.exists(dir) == False:
    os.makedirs(dir)

dfs = tabula.read_pdf(root_dir+filename, pages='all', guess=False)
        
i = 0
for df in dfs:
    df.to_csv(dir+str(i)+'.csv')
    i = i + 1


