import os
import numpy as np
import pandas as pd

owid=pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
covid=pd.read_csv(os.path.join(os.getcwd(),'data/covid.csv'),encoding='utf-8',sep=',')

aIndicator=['total_vaccinations','total_tests','hosp_patients']
dIndicator={'Vaccinations':9,'Tests':10,'Hospitalizations':11}

for e in aIndicator:
    #Formatting data
    df=owid.loc[:,['iso_code','continent','location','date',e]].dropna()
    df.iloc[:,2]=df.iloc[:,2].astype(str)
    df.iloc[:,3]=df.iloc[:,3].astype('datetime64[ns]').dt.strftime('%Y-%m-%d')
    covid.iloc[:,0]=covid.iloc[:,0].astype(str)
    
    df.sort_values(by=['date','location'],inplace=True)
    df.reset_index(inplace=True)
    df.drop(df.columns[0],axis=1,inplace=True)

    #Adding new indicators
    sIndicator=list(dIndicator.keys())[aIndicator.index(e)]
    nIndicator=dIndicator.get(sIndicator)
    covid.insert(nIndicator,sIndicator,0)
    
    #Dictionary for country & region name
    dict_mc={'US':'United States','Taiwan*':'Taiwan'}
    dict_mr={'Macau':'Macao','Faroe Islands':'Faeroe Islands','Falkland Islands (Malvinas)':'Falkland Islands','Saint Helena, Ascension and Tristan da Cunha':'Saint Helena'}

    #Update country name
    for i in list(dict_mc.keys()):
        df1=covid[covid.iloc[:,1]==i].copy()
        for j in df1.index: covid.iloc[j,1]=dict_mc.get(i)

    #Update region name
    for i in list(dict_mr.keys()):
        df1=covid[covid.iloc[:,0]==i].copy()
        for j in df1.index: covid.iloc[j,0]=dict_mr.get(i)

    for i in range(len(df)):
        #country/region & nan
        try:
            covid.iloc[covid[(covid.iloc[:,1]==df.iloc[i,2]) & (covid['Date']==df.iloc[i,3]) & (covid.iloc[:,0]=='nan')].iloc[:,nIndicator].index[0],nIndicator]=df.iloc[i,4]
        except IndexError as e:
            try:
                #province/state
                covid.iloc[covid[(covid.iloc[:,0]==df.iloc[i,2]) & (covid['Date']==df.iloc[i,3])].iloc[:,nIndicator].index[0],nIndicator]=df.iloc[i,4]
            except IndexError as e1:
                try:
                    #country/region with no nan
                    covid.iloc[covid[(covid.iloc[:,1]==df.iloc[i,2]) & (covid['Date']==df.iloc[i,3])].iloc[:,nIndicator].index[0],nIndicator]=df.iloc[i,4]
                except IndexError as e2:
                    pass

covid.to_csv(os.path.join(os.getcwd(),'data/covid.csv'))
#len(dict(zip(np.unique(np.array(covid.iloc[:,9]),return_counts=True))).keys())