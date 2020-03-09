import numpy as np
import pandas as pd
import re

fdc = {'FDC ALARM': 'FDC alarm'}
down = {'DOWN': 'tool down'}
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
                            if value == 'tool down':
                                upper = upper[upper.Date < tmp.Date[0]]
                                tmp = upper.tail(1).reset_index(drop=True)
                                equip = re.split(r' ',comment['Comment'][i])
                                tmp1 = 0
                                for index,k in enumerate(equip):
                                    if 'DOWN' in k.upper():
                                        if index != 0:
                                            if equip[index-1] == tmp.ix[0,'Equip'] or equip[index+1] == tmp.ix[0,'Equip']:
                                                tmp1 = 1
                                                hold_purpose = '當站' + hold_purpose
                                                break
                                        else:
                                            if equip[index+1] == tmp.ix[0,'Equip']:
                                                hold_purpose = '當站' + hold_purpose
                                                tmp1 = 1
                                                break
                                if tmp1 == 0:
                                    hold_purpose = '前站' + hold_purpose

                                #if tmp.ix[0,'Equip'] == 'aassdd':
                                #    hold_purpose = '當站' + hold_purpose

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
    
    
