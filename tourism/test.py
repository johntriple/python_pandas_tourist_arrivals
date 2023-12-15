import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR


# function to download excels from the web
def download_data(url, name):
    dls = url
    resp = requests.get(dls)
    with open(name, 'wb') as output:
        output.write(resp.content)


# The three below normalise functions bring the dataframes to their correct form so they can be merged
def normalise_df1(df):
    df.drop(df.columns[0], axis=1, inplace=True)
    df.rename(columns={'Unnamed: 1': 'country', 'Unnamed: 2': 'planeA', 'Unnamed: 3': 'trainA', 'Unnamed: 4': 'shipA',
                       'Unnamed: 5': 'carA', 'Unnamed: 6': 'sumA'}, inplace=True)
    df.dropna(inplace=True)
    df.set_index('country', inplace=True)


def normalise_df2(df):
    df.drop(df.columns[0], axis=1, inplace=True)
    df.rename(columns={'Unnamed: 1': 'country', 'Unnamed: 2': 'planeB', 'Unnamed: 3': 'trainB', 'Unnamed: 4': 'shipB',
                       'Unnamed: 5': 'carB', 'Unnamed: 6': 'sumB'}, inplace=True)
    df.dropna(inplace=True)
    df.set_index('country', inplace=True)


def normalise_df3(df):
    df.drop(df.columns[0], axis=1, inplace=True)
    df.rename(columns={'Unnamed: 1': 'country', 'Unnamed: 2': 'planeC', 'Unnamed: 3': 'trainC', 'Unnamed: 4': 'shipC',
                       'Unnamed: 5': 'carC', 'Unnamed: 6': 'sumC'}, inplace=True)
    df.dropna(inplace=True)
    df.set_index('country', inplace=True)


# This functions merges three months to a quarter
def merge_df(data1, data2, data3):
    DF = pd.merge(pd.merge(data1, data2, on='country'), data3, on='country', how='left')
    DF.drop(DF.columns[[4, 9, 14]], axis=1, inplace=True)
    DF['total'] = DF.sum(axis=1)
    DF['plane'] = DF['planeA'] + DF['planeB'] + DF['planeC']
    DF['train'] = DF['trainA'] + DF['trainB'] + DF['trainC']
    DF['ship'] = DF['shipA'] + DF['shipB'] + DF['shipC']
    DF['car'] = DF['carA'] + DF['carB'] + DF['carC']
    DF = DF.astype({"total": int, "plane": int, "ship": int, "train": int, "car": int})
    DF.drop(DF.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], axis=1, inplace=True)
    quarterly_total.append(DF.iloc[-1][0])
    return DF


# 2011
download_data(
    "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113865&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
    "2011.xls")
# 2012
download_data(
    "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113886&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
    "2012.xls")
# 2013
download_data(
    "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113905&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
    "2013.xls")
# 2014
download_data(
    "https://www.statistics.gr/el/statistics?p_p_id=documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=4&p_p_col_pos=2&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_javax.faces.resource=document&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_ln=downloadResources&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_documentID=113925&_documents_WAR_publicationsportlet_INSTANCE_VBZOni0vs5VJ_locale=el",
    "2014.xls")

# Pandas functions to display all the rows and columns of a dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

total_plane = 0  # total number of tourists arriving by plane will be stored here
total_ship = 0  # total number of tourists arriving by ship will be stored here
total_car = 0  # total number of tourists arriving by car will be stored here
total_train = 0  # total number of tourists arriving by train will be stored here
quarterly_total = []  # total number of tourists arriving every quarter of the year will be stored here
transports = []  # this list will be used to temporarily hold the means of transport variables and will later be transformed into a Series
sum_until_quarter = []  # the sum of the total number of turists until this quarter will be stored in this quarter

# 1st Quarter 2011
xls_file = pd.ExcelFile('2011.xls')

# creating three dataframes that will be holding 1 month each that will be changing every quarter
df1 = xls_file.parse('ΙΑΝ')
df1 = df1[6:66]
df2 = xls_file.parse('ΦΕΒ')
df2 = df2[6:66]
df3 = xls_file.parse('ΜΑΡ')
df3 = df3[6:66]
df3.iloc[-4][2] = 0  # changing Nan value to 0

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)

DFA = merge_df(df1, df2, df3)
total_plane = total_plane + DFA.iloc[-1][1]  # adding the total numbers of tourists that arrived by plane this quarter
total_train = total_train + DFA.iloc[-1][2]  # adding the total numbers of tourists that arrived by train this quarter
total_ship = total_ship + DFA.iloc[-1][3]  # adding the total numbers of tourists that arrived by ship this quarter
total_car = total_car + DFA.iloc[-1][4]  # adding the total numbers of tourists that arrived by car this quarter

# 2nd quarter 2011

df1 = xls_file.parse('ΑΠΡ')
df1 = df1[6:66]
df2 = xls_file.parse('ΜΑΙ')
df2 = df2[6:66]
df3 = xls_file.parse('ΙΟΥΝ')
df3 = df3[6:66]
df3.iloc[-5][-2] = 0  # dataset australia is Nan this makes it 0

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFB = merge_df(df1, df2, df3)

total_plane = total_plane + DFB.iloc[-1][1]
total_train = total_train + DFB.iloc[-1][2]
total_ship = total_ship + DFB.iloc[-1][3]
total_car = total_car + DFB.iloc[-1][4]

# 3rd quarter 2011

df1 = xls_file.parse('ΙΟΥΛ')
df1 = df1[6:66]
df2 = xls_file.parse('ΑΥΓ')
df2 = df2[6:66]
df2.iloc[0][-2] = 0  # correcting austria
df2.iloc[41][-2] = 0  # correcting loipa krati M.anatolis
df3 = xls_file.parse('ΣΕΠ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFC = merge_df(df1, df2, df3)

total_plane = total_plane + DFC.iloc[-1][1]
total_train = total_train + DFC.iloc[-1][2]
total_ship = total_ship + DFC.iloc[-1][3]
total_car = total_car + DFC.iloc[-1][4]

# 4th quarter 2011   

df1 = xls_file.parse('ΟΚΤ')
df1 = df1[6:66]
df2 = xls_file.parse('ΝΟΕ')
df2 = df2[6:66]
df3 = xls_file.parse('ΔΕΚ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFD = merge_df(df1, df2, df3)
total_plane = total_plane + DFD.iloc[-1][1]
total_train = total_train + DFD.iloc[-1][2]
total_ship = total_ship + DFD.iloc[-1][3]
total_car = total_car + DFD.iloc[-1][4]

# unifying the 4 dataframes on the country column and getting rid of anything else
DFA.drop(DFA.tail(1).index, inplace=True)
DFA.drop(DFA.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFA.loc['Κροατία'] = [
    0]  # inserting Croatia to the dataframe so I can merge the years that have it as one of their rows(2013-2014)with the ones that dont(2011-2012)
DFA.rename(columns={'total': 'totalA'}, inplace=True)

DFB.drop(DFB.tail(2).index, inplace=True)
DFB.drop(DFB.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFB.loc['Κροατία'] = [0]
DFB.rename(columns={'total': 'totalB'}, inplace=True)

DFC.drop(DFC.tail(1).index, inplace=True)
DFC.drop(DFC.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFC.loc['Κροατία'] = [0]
DFC.rename(columns={'total': 'totalC'}, inplace=True)

DFD.drop(DFD.tail(1).index, inplace=True)
DFD.drop(DFD.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFD.loc['Κροατία'] = [0]
DFD.rename(columns={'total': 'totalD'}, inplace=True)

# merging the 12 months to a year
DF11 = pd.merge(pd.merge(pd.merge(DFA, DFB, on='country'), DFC, on='country'), DFD, on='country', how='left')
DF11['total_11'] = DF11['totalA'] + DF11['totalB'] + DF11['totalC'] + DF11['totalD']
DF11.drop(DF11.columns[[0, 1, 2, 3]], axis=1, inplace=True)

# 1st quarter 2012
xls_file = pd.ExcelFile('2012.xls')

df1 = xls_file.parse('ΙΑΝ')
df1 = df1[6:66]
df2 = xls_file.parse('ΦΕΒ')
df2 = df2[6:66]
df3 = xls_file.parse('ΜΑΡ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFA = merge_df(df1, df2, df3)
total_plane = total_plane + DFA.iloc[-1][1]
total_train = total_train + DFA.iloc[-1][2]
total_ship = total_ship + DFA.iloc[-1][3]
total_car = total_car + DFA.iloc[-1][4]

# 2nd quarter 2012

df1 = xls_file.parse('ΑΠΡ')
df1 = df1[6:66]
df2 = xls_file.parse('ΜΑΙΟΣ')
df2 = df2[6:66]
df3 = xls_file.parse('ΙΟΥΝ')
df3 = df3[6:66]
normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFB = merge_df(df1, df2, df3)
total_plane = total_plane + DFB.iloc[-1][1]
total_train = total_train + DFB.iloc[-1][2]
total_ship = total_ship + DFB.iloc[-1][3]
total_car = total_car + DFB.iloc[-1][4]

# 3rd quarter 2012

df1 = xls_file.parse('ΙΟΥΛ')
df1 = df1[6:66]
df2 = xls_file.parse('ΑΥΓ')
df2 = df2[6:66]
df3 = xls_file.parse('ΣΕΠΤ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)

DFC = merge_df(df1, df2, df3)
total_plane = total_plane + DFC.iloc[-1][1]
total_train = total_train + DFC.iloc[-1][2]
total_ship = total_ship + DFC.iloc[-1][3]
total_car = total_car + DFC.iloc[-1][4]

# 4th quarter 2012

df1 = xls_file.parse('ΟΚΤ')
df1 = df1[6:66]
df2 = xls_file.parse('ΝΟΕΜ')
df2 = df2[6:66]
df3 = xls_file.parse('ΔΕΚ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)

DFD = merge_df(df1, df2, df3)
total_plane = total_plane + DFD.iloc[-1][1]
total_train = total_train + DFD.iloc[-1][2]
total_ship = total_ship + DFD.iloc[-1][3]
total_car = total_car + DFD.iloc[-1][4]

# ynifying the 4 dataframes of 2012 on the country column and getting rid of anything else

DFA.drop(DFA.tail(1).index, inplace=True)
DFA.drop(DFA.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFA.loc['Κροατία'] = [0]
DFA.rename(columns={'total': 'totalA'}, inplace=True)

DFB.drop(DFB.tail(2).index, inplace=True)
DFB.drop(DFB.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFB.loc['Κροατία'] = [0]
DFB.rename(columns={'total': 'totalB'}, inplace=True)

DFC.drop(DFC.tail(1).index, inplace=True)
DFC.drop(DFC.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFC.loc['Κροατία'] = [0]
DFC.rename(columns={'total': 'totalC'}, inplace=True)

DFD.drop(DFD.tail(1).index, inplace=True)
DFD.drop(DFD.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFD.loc['Κροατία'] = [0]
DFD.rename(columns={'total': 'totalD'}, inplace=True)

DF12 = pd.merge(pd.merge(pd.merge(DFA, DFB, on='country'), DFC, on='country'), DFD, on='country', how='left')
DF12['total_12'] = DF12['totalA'] + DF12['totalB'] + DF12['totalC'] + DF12['totalD']
DF12.drop(DF12.columns[[0, 1, 2, 3]], axis=1, inplace=True)

# changing excel to 2013
xls_file = pd.ExcelFile('2013.xls')

# 1st quarter 2013

df1 = xls_file.parse('ΙΑΝ')
df1 = df1[6:66]
df2 = xls_file.parse('ΦΕΒ')
df2 = df2[6:66]
df3 = xls_file.parse('ΜΑΡ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFA = merge_df(df1, df2, df3)
total_plane = total_plane + DFA.iloc[-1][1]
total_train = total_train + DFA.iloc[-1][2]
total_ship = total_ship + DFA.iloc[-1][3]
total_car = total_car + DFA.iloc[-1][4]

# 2nd quarter 2013
df1 = xls_file.parse('ΑΠΡ')
df1 = df1[6:66]
df2 = xls_file.parse('ΜΑΙΟΣ')
df2 = df2[6:66]
df3 = xls_file.parse('ΙΟΥΝ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFB = merge_df(df1, df2, df3)
total_plane = total_plane + DFB.iloc[-1][1]
total_train = total_train + DFB.iloc[-1][2]
total_ship = total_ship + DFB.iloc[-1][3]
total_car = total_car + DFB.iloc[-1][4]

# 3rd quarter 2013
df1 = xls_file.parse('ΙΟΥΛ')
df1 = df1[6:66]
df2 = xls_file.parse('ΑΥΓ')
df2 = df2[6:66]
df3 = xls_file.parse('ΣΕΠ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFC = merge_df(df1, df2, df3)
total_plane = total_plane + DFC.iloc[-1][1]
total_train = total_train + DFC.iloc[-1][2]
total_ship = total_ship + DFC.iloc[-1][3]
total_car = total_car + DFC.iloc[-1][4]

# 4th quarter 2013

df1 = xls_file.parse('ΟΚΤ')
df1 = df1[6:66]
df1.iloc[11][-4] = 0  # correcting croatia
df2 = xls_file.parse('ΝΟΕ')
df2 = df2[6:66]
df2.iloc[11][-4] = 0  # correcting croatia
df3 = xls_file.parse('ΔΕΚ')
df3 = df3[6:66]
df3.iloc[11][-4] = 0  # correcting croatia

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFD = merge_df(df1, df2, df3)
total_plane = total_plane + DFD.iloc[-1][1]
total_train = total_train + DFD.iloc[-1][2]
total_ship = total_ship + DFD.iloc[-1][3]
total_car = total_car + DFD.iloc[-1][4]

# unifying the dataframes of 2013 on the country column and getting rid of anything else

DFA.drop(DFA.tail(1).index, inplace=True)
DFA.drop(DFA.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFA.loc['Κροατία (2)'] = [0]
DFA.rename(columns={'total': 'totalA'}, inplace=True)

DFB.drop(DFB.tail(2).index, inplace=True)
DFB.drop(DFB.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFB.loc['Κροατία (2)'] = [0]
DFB.rename(columns={'total': 'totalB'}, inplace=True)

DFC.drop(DFC.tail(1).index, inplace=True)
DFC.drop(DFC.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFC.rename(columns={'total': 'totalC'}, inplace=True)

DFD.drop(DFD.tail(1).index, inplace=True)
DFD.drop(DFD.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFD.rename(columns={'total': 'totalD'}, inplace=True)

DF13 = pd.merge(pd.merge(pd.merge(DFA, DFB, on='country'), DFC, on='country'), DFD, on='country', how='left')
DF13['total_13'] = DF13['totalA'] + DF13['totalB'] + DF13['totalC'] + DF13['totalD']
DF13.drop(DF13.columns[[0, 1, 2, 3]], axis=1, inplace=True)
DF13 = DF13.rename(index={"Κροατία (2)": "Κροατία"})  # renaming the index of croatia to what it should have always been

# changing excel to 2014
xls_file = pd.ExcelFile('2014.xls')

# 1st quarter of 2014

df1 = xls_file.parse('ΙΑΝ')
df1 = df1[6:66]
df2 = xls_file.parse('ΦΕΒ')
df2 = df2[6:66]
df3 = xls_file.parse('ΜΑΡ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFA = merge_df(df1, df2, df3)
DFA = DFA.rename(index={"Κροατία (2)": "Κροατία"})
total_plane = total_plane + DFA.iloc[-1][1]
total_train = total_train + DFA.iloc[-1][2]
total_ship = total_ship + DFA.iloc[-1][3]
total_car = total_car + DFA.iloc[-1][4]

# 2nd quarter of 2014

df1 = xls_file.parse('ΑΠΡ')
df1 = df1[6:66]
df2 = xls_file.parse('ΜΑΙ')
df2 = df2[6:66]
df3 = xls_file.parse('ΙΟΥΝ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFB = merge_df(df1, df2, df3)
DFB = DFB.rename(index={"Κροατία (2)": "Κροατία"})
total_plane = total_plane + DFB.iloc[-1][1]
total_train = total_train + DFB.iloc[-1][2]
total_ship = total_ship + DFB.iloc[-1][3]
total_car = total_car + DFB.iloc[-1][4]

# 3rd quarter of 2014

df1 = xls_file.parse('ΙΟΥΛ')
df1 = df1[6:66]
df2 = xls_file.parse('ΑΥΓ')
df2 = df2[6:66]
df3 = xls_file.parse('ΣΕΠΤ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFC = merge_df(df1, df2, df3)
DFC = DFC.rename(index={"Κροατία (1)": "Κροατία"})
total_plane = total_plane + DFC.iloc[-1][1]
total_train = total_train + DFC.iloc[-1][2]
total_ship = total_ship + DFC.iloc[-1][3]
total_car = total_car + DFC.iloc[-1][4]

# 4th quarter of 2014

df1 = xls_file.parse('ΟΚΤ')
df1 = df1[6:66]
df2 = xls_file.parse('ΝΟΕΜ')
df2 = df2[6:66]
df3 = xls_file.parse('ΔΕΚ')
df3 = df3[6:66]

normalise_df1(df1)
normalise_df2(df2)
normalise_df3(df3)
DFD = merge_df(df1, df2, df3)
DFD = DFD.rename(index={"Κροατία (1)": "Κροατία"})
total_plane = total_plane + DFD.iloc[-1][1]
total_train = total_train + DFD.iloc[-1][2]
total_ship = total_ship + DFD.iloc[-1][3]
total_car = total_car + DFD.iloc[-1][4]

# unifying the dataframes of 2014 on the country column and getting rid of anything else

DFA.drop(DFA.tail(1).index, inplace=True)
DFA.drop(DFA.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFA.rename(columns={'total': 'totalA'}, inplace=True)

DFB.drop(DFB.tail(2).index, inplace=True)
DFB.drop(DFB.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFB.rename(columns={'total': 'totalB'}, inplace=True)

DFC.drop(DFC.tail(1).index, inplace=True)
DFC.drop(DFC.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFC.rename(columns={'total': 'totalC'}, inplace=True)

DFD.drop(DFD.tail(1).index, inplace=True)
DFD.drop(DFD.columns[[1, 2, 3, 4]], axis=1, inplace=True)
DFD.rename(columns={'total': 'totalD'}, inplace=True)

DF14 = pd.merge(pd.merge(pd.merge(DFA, DFB, on='country'), DFC, on='country'), DFD, on='country', how='left')
DF14['total_14'] = DF14['totalA'] + DF14['totalB'] + DF14['totalC'] + DF14['totalD']
DF14.drop(DF14.columns[[0, 1, 2, 3]], axis=1, inplace=True)

# unifying the dataframes of 2011-2014 to find out the total number of tourists that arrived to greece from each country

DF = pd.merge(pd.merge(pd.merge(DF11, DF12, on='country'), DF13, on='country'), DF14, on='country', how='left')
DF['total_tourists'] = DF['total_11'] + DF['total_12'] + DF['total_13'] + DF['total_14']
DF.drop(DF.columns[[0, 1, 2, 3]], axis=1, inplace=True)
DF = DF.sort_values(by='total_tourists', ascending=True)

transports.append(total_plane)
transports.append(total_car)
transports.append(total_ship)
transports.append(total_train)

# appending the list that contains the number of tourists until a given quarter
for i in range(16):
    if (i == 0):
        sum_until_quarter.append(quarterly_total[i])
    else:
        sum_until_quarter.append(sum_until_quarter[i - 1] + quarterly_total[i])

# creating the graph for transports
transport_labels = ['plane', 'car', 'ship', 'train']
plt.figure(1)
plt.ticklabel_format(style='plain')
bars_transports = plt.bar(transport_labels, transports, width=0.3)
plt.title("Distribution of tourists that arrived to greece by transport (2011-2014)")
plt.ylabel('Tourists')
plt.yticks(np.arange(0, 55000000, step=5000000))
plt.savefig("transports.png", dpi=300, bbox_inches='tight')

# creating graph for total tourists per quarter
quarter_labels = ['Q1-2011', 'Q2-2011', 'Q3-2011', 'Q4-2011', 'Q1-2012', 'Q2-2012', 'Q3-2012', 'Q4-2012', 'Q1-2013',
                  'Q2-2013', 'Q3-2013', 'Q4-2013', 'Q1-2014', 'Q2-2014', 'Q3-2014', 'Q4-2014']
plt.figure(2, figsize=(14, 5))
plt.ticklabel_format(style='plain')
plt.title("Tourists per quarter (2011-2014)")
plt.ylabel("Tourists")
plt.xlabel("Quarter")
bars_quarters = plt.bar(quarter_labels, quarterly_total)
plt.savefig("quarter.png", dpi=300, bbox_inches='tight')

# creating graph displaying the total number of tourists that arrived to greece from 2011 until a give quarter
plt.figure(3, figsize=(14, 8))
plt.ticklabel_format(style="plain")
plt.title("Total number of tourists that arrived to greece until a given quarter over time ")
plt.ylabel("Tourists")
plt.xlabel("Quarter")
plt.xticks([1, 3, 5, 7, 9, 11, 13, 15])
plt.plot(quarter_labels, sum_until_quarter, 'r.-')
plt.savefig("total-tourists-until-given-quarter.png", dpi=300, bbox_inches='tight')

# creating a graph that shows how many tourists greece had from each country during the years 2011-2015

plt.figure(4, figsize=(10, 12))
plt.ticklabel_format(style="plain")
plt.title("Total number of tourists for every country")
plt.xticks(np.arange(0, 10000000, step=1000000))
plt.xlabel("Tourists")
plt.barh(DF.index, DF.total_tourists)
plt.savefig("tourists-country.png", dpi=300, bbox_inches='tight')

# creating dataframes so I can extreact them to csv
Total_sum_quarter = pd.DataFrame(data=sum_until_quarter, index=quarter_labels)
Total_sum_quarter.index.names = ['Quarter']
Total_sum_quarter.rename(columns={0: 'tourists visited thus far'}, inplace=True)

Tourism_per_quarter = pd.DataFrame(data=quarterly_total, index=quarter_labels)
Tourism_per_quarter.index.names = ['Quarter']
Tourism_per_quarter.rename(columns={0: 'tourists visited'}, inplace=True)

dftransports = pd.DataFrame(data=transports, index=transport_labels)
dftransports.index.names = ['Transport']
dftransports.rename(columns={0: 'tourists'}, inplace=True)

# making the csvs
DF.to_csv(r'./country-tourism.csv')
Total_sum_quarter.to_csv(r'./Quarter-sum_total.csv')
Tourism_per_quarter.to_csv(r'./Tourists_per_quarter.csv')
dftransports.to_csv(r'./Transports-tourist.csv')

# inserting the dataframes to MySQL database

engine = create_engine("mysql+pymysql://root:1zcyasYNtm@127.0.0.1/Tourism")
con = engine.connect()
DF.to_sql(name='countries', con=con, if_exists='replace', dtype={'country': VARCHAR(55)})
Total_sum_quarter.to_sql(name='tourists_until_quarter', con=con, if_exists='replace', dtype={'Quarter': VARCHAR(25)})
dftransports.to_sql(name='transports', con=con, if_exists='replace', dtype={'Transport': VARCHAR(20)})
Tourism_per_quarter.to_sql(name='tourists_per_quarter', con=con, if_exists='replace', dtype={'Quarter': VARCHAR(25)})
print('success')
print('git')