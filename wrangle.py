import numpy as np
import pandas as pd
import pycountry_convert as pc

def get_continent(country):
    try:
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format='default')
        return pc.country_alpha2_to_continent_code(country_code)
    except (KeyError, TypeError):
        return country

def wrangle_data(covid_df, pop_df):
    covid_df = covid_df.assign(Date=covid_df['Date'].astype(np.datetime64))
    covid_df['Longitude'] = covid_df['Long']
    covid_df['Latitude'] = covid_df['Lat']
    covid_df['Country'] = covid_df['Country/Region'].fillna('')
    covid_df['Country'] = covid_df['Country']
    covid_df['Continent'] = covid_df['Country'].apply(get_continent)

    covid_df = covid_df.merge(pop_df, how='left', left_on='Country', right_on='Country')
    covid_df['State'] = covid_df['Province/State'].fillna(covid_df['Country'])
    covid_df['StateCountry'] = covid_df['State'] + ' ' + covid_df['Country']
    covid_df['Active'] = covid_df['Confirmed'] - covid_df['Recovered']

    per_capita_adjust = 100000.0

    def per_capita(col):
        return (
                covid_df[col]
                / covid_df['Population']
                * per_capita_adjust
        ).round(0)
    

def logs(x):
    if x > 0:
        return np.log10(x)
    else:
        return 0

    covid_df['ActivePerCapita'] = per_capita('Active')
    covid_df['ConfirmedPerCapita'] = per_capita('Confirmed')
    covid_df['RecoveredPerCapita'] = per_capita('Recovered')
    covid_df['DeathsPerCapita'] = per_capita('Deaths')
    covid_df['TestsPerCapita'] = per_capita('Tests')
    covid_df['VaccinationsPerCapita'] = per_capita('Vaccinations')
    covid_df['HospitalizationsPerCapita'] = per_capita('Hospitalizations')
    covid_df['log10'] = covid_df['Confirmed'].map(logs)
    covid_df['log_group'] = np.power(10, covid_df['log10'] - 1).astype(np.int).astype(str) \
                            + '-' + np.power(10, covid_df['log10']).astype(np.int).astype(str)
    covid_df['Description'] = covid_df['State'] + ', ' \
                              + covid_df['Country'] + ', ' \
                              + covid_df['Continent'] + '<br>' \
                              + 'Confirmed: ' + covid_df['Confirmed'].astype(str) + '<br>' \
                              + 'Confirmed Per Capita: ' + covid_df['ConfirmedPerCapita'].astype(str) + '<br>' \
                              + 'Recovered: ' + covid_df['Recovered'].astype(str) + '<br>' \
                              + 'Active: ' + covid_df['Active'].astype(str) + '<br>' \
                              + 'Deaths: ' + covid_df['Deaths'].astype(str) + '<br>' \
                              + 'Tests: ' + covid_df['Tests'].astype(str) + '<br>' \
                              + 'Vaccinations: ' + covid_df['Vaccinations'].astype(str) + '<br>' \
                              + 'Hospitalizations: ' + covid_df['Hospitalizations'].astype(str) + '<br>' \
                              + 'Confirmed Range: ' + covid_df['log_group'].astype(str) + '<br>'
    return covid_df

def indicator_barplot(covid_df, count_col='Confirmed'):
    #check & drop unnamed column if exist
    if any('name' in i for i in covid_df.columns): df=covid_df.drop(covid_df.columns[0],axis=1).copy()
    #get data by indicator & adjust the format date
    df=df.loc[:,['Country',count_col,'Date']].copy()
    #formatting date
    df=df[df[count_col]>0]
    df.sort_values(by=['Date'],inplace=True)
    df['Month']=df['Date'].astype('datetime64[ns]').dt.strftime('%Y-%m')
    df.reset_index(inplace=True)
    df.drop(df.columns[0],axis=1, inplace=True)  
    #group by indicator
    dfupd=pd.DataFrame([])
    for i in df.iloc[:,0].unique():
        for j in df.iloc[:,3].unique():
            try:
                sMaxDate=df[(df.iloc[:,0]==i) & (df['Month']==j)].groupby(['Country','Date','Month']).size().reset_index().sort_values(by=['Date'],ascending=False).head(1)['Date'].values[0]
                dftmp=df[(df.iloc[:,0]==i) & (df['Month']==j) & (df['Date']==sMaxDate)].groupby(['Country','Date','Month']).sum().reset_index().copy()
                dfupd=pd.concat([dfupd,dftmp],axis=0)
            except IndexError as e:
                pass
    #sort & get top 10 per indicator
    dfnew=pd.DataFrame([])
    dfupd=dfupd.sort_values(by=['Month',count_col],ascending=True)
    for i in dfupd['Month'].unique():
        dfnew=pd.concat([dfnew,dfupd[dfupd.iloc[:,2]==i].sort_values(by=[count_col],ascending=False).head(10)],axis=0)
    return dfnew.drop(dfnew.columns[1],axis=1)

def sunburst_df(df, policy = 'Stay-at-Home Requirements'):
    sunburst = df[df['Day']=='2021-03-13'][['Entity',policy]]
    sunburst.drop_duplicates(inplace=True)
    sunburst.reset_index(drop=True, inplace=True)
    sunburst.insert(2,'Day', "")
    latest_measure = [(country, df[(df['Entity']==country) & (df['Day']=='2021-03-13')][policy].tolist()[0]) for country in df[df['Day']=='2021-03-13']['Entity'].unique()]
    for country, measure in latest_measure:
        try:
            sdate = df[(df.iloc[:, 0]==country) & (df[policy]==measure) & (df['Day'].str.contains('2021'))].head(1)['Day'].values[0]
            index = sunburst[(sunburst.iloc[:, 0]==country) & (sunburst.iloc[:, 1]==measure)].index[0]
            sunburst.iloc[index, 2]=sdate
        except IndexError:
            pass
    return sunburst