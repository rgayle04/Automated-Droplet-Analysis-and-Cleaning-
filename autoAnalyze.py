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

def analyze(csv_path, output_path):
    name = Path(csv_path).stem
    df = pd.read_csv(csv_path)
    os.makedirs(output_path, exist_ok=True)
    if df.empty:
        return
    else:

        std = np.std(df['DIB Radius'], ddof= 1)
        print('DIB Rad Standard Deviation:', std)
        mean = df['DIB Radius'].mean()
        print('DIB Rad Mean:', mean)

        uL = mean + (std*3) 
        lL = mean - (std*3)

        #outliers = np.where((df['DIB Radius']> uL) | (df['DIB Radius'] < lL))

        outliers = np.where((df['DIB Radius']> uL) & (df['DIB Radius'] < lL))
        
        df.drop(outliers[0], axis=0, inplace=True)

        split_name = name.split(" ")
        
        sp_name = split_name[-1]

        osmP = ""

        for i in range(3):
            if len(osmP)<3:
                osmP+=sp_name[i]
        #print(int(osmP))
        
        osmP = float(osmP)/1000

        df['Org. Concentr'] = None

        df.at[0, 'Org. Concentr'] = osmP

        df['Adjusted Time'] = (df['Time Stamp']-df.loc[0, 'Time Stamp'])

        df['DIB Area'] =  math.pi*(df.loc[0,'DIB Radius']**2)
        
        av = df.loc[0, 'Droplet 1 Volume']
        
        df['(V/V0)^2']= (df['Droplet 1 Volume']/av)**2

        df['Linear Permebility Section:'] = None 

        df['Init Radius'] = None
        df.at[0, 'Init Radius'] = (df.loc[0,'Droplet 1 Radius']/10000)

        f = (df.loc[1,'Droplet 1 Radius']/10000) 

        df['Init Vol'] = None
        df.at[0, 'Init Vol'] = (4/3)*3.1415*(df.loc[0,'Init Radius']**3)

        df['Linearized DIB Radius'] = None
        slope, intercept, r, p, std_error = stats.linregress(df['Adjusted Time'], df['DIB Radius'])

        df.at[0, 'Linearized DIB Radius'] = intercept

        df['DIB Radius(cm)'] = None
        df.at[0, 'DIB Radius(cm)'] = intercept/10000

        df['DIB Area(cm^2)'] = None
        df.at[0, 'DIB Area(cm^2)'] = math.pi*(df.loc[0,'DIB Radius(cm)']**2)

        slope, intercept, r, p, std_error = stats.linregress(df['Adjusted Time'], df['(V/V0)^2'])
        
        df['slope (V/V0)^2'] = None
        df.at[0, 'slope (V/V0)^2'] = slope

        df['r^2'] = None
        df.at[0, 'r^2'] = intercept

        df['Permeability (avg DIB Rad)'] = None 

        df.at[0, 'Permeability (avg DIB Rad)'] = ((slope/2)* df.loc[0, 'DIB Radius(cm)'])/(df.loc[0, 'DIB Area(cm^2)']*0.018*df.loc[0,'Org. Concentr'])*2

        df['3rd Degree Polynomial Section:'] = None

        X_poly = np.vstack([df['Adjusted Time']**1, df['Adjusted Time']**2, df['Adjusted Time']**3]).T
        model = LinearRegression()
        model.fit(X_poly, df['DIB Area'])
        coefficients = model.coef_
        intercept = model.intercept_

        a = coefficients.tolist() 
        df['A'] = None
        df.at[0, 'A'] = a[0]
        df['B'] = None
        df.at[0, 'B'] = a[1]
        df['C'] = None
        df.at[0, 'C'] = a[2]
        df['D'] = None
        df.at[0, 'D'] = intercept 
        df['Eval']=((0.018*df.loc[0, 'Org. Concentr']*df.loc[0, 'A']*df['Adjusted Time']**4)/(2*df.loc[0, 'Droplet 1 Volume'])+(2*0.018*df.loc[0, 'Org. Concentr']*df.loc[0, 'B']*df['Adjusted Time']**3)/(3*df.loc[0,'Droplet 1 Volume'])+(0.018*df.loc[0, 'Org. Concentr']*df.loc[0, 'C']*df['Adjusted Time']**2)/df.loc[0,'Droplet 1 Volume']+(2*0.018*df.loc[0, 'Org. Concentr']*df.loc[0, 'D']*df['Adjusted Time'])/df.loc[0,'Droplet 1 Volume'])

        
        #df.at[0, 'Permeability'] = ((slope/2)* df.loc[0, 'DIB Radius(cm)'])/(df.loc[0, 'DIB Area(cm^2)']*0.018*(df.loc[0, 'Org. Concentr']))

        
        slope, intercept, r, p ,std_error = stats.linregress(df['Eval'], df['(V/V0)^2'])
        df['Permeability (slope)']= None
        df.at[0, 'Permeability (slope)'] = slope

        df['Permeability (intercept)'] = None
        df.at[0, 'Permeability (intercept)'] = intercept

        df.to_csv(csv_path, index=False)

        print(f'[DONE] {name} processed. \n')

def main(csv_path, output_path):
    if os.path.isdir(csv_path):
        csvFiles = []
        for ext in extensions:
            csvFiles.extend(glob.glob(os.path.join(csv_path, ext)))
        for csv in csvFiles:
            analyze(csv, output_path)
    else:
        analyze(csv_path, output_path)

if __name__ == "__main__":
    
    csv_path = sys.argv[1]

    output_path = sys.argv[2]

    main(csv_path, output_path)