import numpy as np
import pandas as pd

fdc = {'FDC ALARM': 'FDC alarm'}
down = {'DOWN': 'Tool Down'}
pilot = {'PILOT': 'Tool/BKM pilot'}
rule = [fdc, down, pilot]

if __name__ == '__main__':
    df = pd.read_csv('CSV.csv')
    #df['Date'] = df['Date'].astype('datetime64[ns]')
    df.Date = pd.to_datetime(df.Date)
    target = pd.to_datetime('2019-03-13')

    if (df.Date == target).any():
        isget = False
        upper = df[df.Date < target]
        lower = df[df.Date > target]
        while ((upper.Date < target).any()) and isget == False:
            tmp = upper.tail(1).reset_index(drop=True)
            #print(tmp.Date)
            comment = upper[upper.Date == tmp.Date[0]].reset_index(drop=True)

            for i in range(len(comment)):
                for r in rule:
                    for key, value in r.items():
                        if key in comment['Comment'][i].upper():
                            isget = True
                            hold_purpose = key
                            hold_time = tmp
                            break
                    if isget: break
                if isget: break    
            upper = upper[upper.Date < tmp.Date[0]]

        while ((lower.Date > target).any()) and isget == False:
            tmp = lower.head(1).reset_index(drop=True)
            comment = lower[lower.Date == tmp.Date[0]].reset_index(drop=True)
            for i in range(len(comment)):
                for r in rule:
                    for key, value in r.items():
                        if key in comment['Comment'][i].upper():
                            isget = True
                            hold_purpose = key
                            hold_time = tmp
                            break
                    if isget: break
                if isget: break    
            lower = lower[lower.Date > tmp.Date[0]]


        if isget: 
            print(hold_time.Date[0], hold_purpose)

            #print(comment)
            #print(comment)
            

    #print(df[df.Date>target].iloc[0])
    
    
