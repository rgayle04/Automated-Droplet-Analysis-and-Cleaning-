import os
import math 
import pandas as pd 
import glob
import numpy as np
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import sys
from pathlib import Path



extensions = ['*.csv','*.xl','*.xlsx', '*.xlsm']



def swiffer(csv_path):
    #os.makedirs(opath, exist_ok=True)
    print(f'{csv_path}')

    
    df = pd.read_csv(csv_path)
    name = Path(csv_path).stem 
    print(f'Original Rows: {len(df)}')

    #print(f'{int(df.isna().sum())} instances of NaN data in {name}')
    print(f'Cleaning {name}...')
    for col in df.columns: 
        before = len(df)
        df2 = df[~df[col].astype(str).str.contains('-nan\(ind\)|#NAME\?', regex=True, case=False, na=False)]
        after = len(df2)
        if before != after:
            print(f'Removed {(before - after)} rows from column {col}')
    #df = df.dropna(inplace=True)

    print(f'Cleaned Rows: {len(df)}')
    excel_path = csv_path.replace('.csv', '.xlsx')
    df.to_excel(csv_path, index=False)
    



def main(csv_path):
    if os.path.isdir(csv_path):
        csvFiles = []
        for ext in extensions:
            csvFiles.extend(glob.glob(os.path.join(csv_path, ext)))
        for file in csvFiles:
            swiffer(file)
    else:
        swiffer(csv_path)

if __name__=="__main__":
    csv_path = sys.argv[1]
    #opath = sys.argv[2]

    main(csv_path)
    

