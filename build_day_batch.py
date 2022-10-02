import numpy as np
import pandas as pd
from spacepy import pycdf


def build_day_BD(cdf):

    Bd = cdf.copy()
    Bdkeys = list(Bd.keys())

    for key in Bdkeys:
        if key not in ['Time1_PB5', 'B1F1', 'B1GSE', 'FLAG1']:
            del Bd[key]

    Bd['Time1_PB5'] = Bd['Time1_PB5'][:,2:].reshape(-1,)
    Bd['B1GSE_x'] = Bd['B1GSE'][:,:1].reshape(-1,)
    Bd['B1GSE_y'] = Bd['B1GSE'][:,1:2].reshape(-1,)
    Bd['B1GSE_z'] = Bd['B1GSE'][:,2:3].reshape(-1,)

    del Bd['B1GSE']

    return pd.DataFrame(Bd)


def build_day_WI(cdf):

    wind_ion = cdf.copy()
    wind_ionkeys = list(wind_ion.keys())

    for key in wind_ionkeys:
        if key not in ['Proton_Np_nonlin', 'Proton_V_nonlin', 'Proton_W_nonlin']:
            del wind_ion[key]

    return pd.DataFrame(wind_ion)


# def build_day_BW(cdf):

#     Bw = cdf.copy()
#     Bwkeys = list(Bw.keys())

#     for key in Bwkeys:
#         if key not in ['Time_PB5', 'BF1', 'BGSE']:
#             del Bw[key]

#     Bw['Time_PB5'] = Bw['Time_PB5'][:,2:].reshape(-1,)
#     Bw['BGSE_z'] = Bw['BGSE'][:,2:3].reshape(-1,)
#     Bw['BGSE_x'] = Bw['BGSE'][:,:1].reshape(-1,)
#     Bw['BGSE_y'] = Bw['BGSE'][:,1:2].reshape(-1,)

#     Bw['BF1'] = Bw['BF1'].reshape(-1,)

#     del Bw['BGSE']


#     return pd.DataFrame(Bw)



# def undersample_BW(Bw):

#     new_Bw = pd.DataFrame()

#     for i in range(0,len(Bw), 11):
#         new_Bw = pd.concat([new_Bw, pd.DataFrame([pd.DataFrame(Bw).iloc[i]])])
#         print(f'On Entry# {i+1} ')

#     return new_Bw


# def dtw_alt(Bd, Bw):
    
#     Bw = undersample_BW(Bw)

#     if Bw.shape[0] < Bd.shape[0]:
        
#         diff = len(Bd) - len(Bw)
#         factor = len(Bd) // diff

#         for i in range(0, len(Bd), factor):
#             try:
#                 Bd.drop(i, inplace=True)
#             except: print("Not found in axis")

#     if Bw.shape[0] > Bd.shape[0]:
        
#         diff = len(Bw) - len(Bd)
#         factor = len(Bw) // diff

#         for i in range(0, len(Bw), factor):
#             try:
#                 Bw.drop(i, inplace=True)
#             except: print("Not found in axis")

#     print(Bw.shape)
#     print(Bd.shape)

#     Bd.drop(Bd[Bd['FLAG1'] == 1], inplace=True)

#     return Bd


def merge_DFs(Bd, WI):

    merged_df = pd.DataFrame()
    factor = len(Bd) // len(WI)

    Bd_idx = 0
    for i in range(len(WI)):
        temp_df = pd.concat([pd.DataFrame([Bd.iloc[Bd_idx]]).reset_index(), pd.DataFrame([WI.iloc[i]]).reset_index()], axis=1)
        # print(temp_df)
        merged_df = pd.concat([merged_df, temp_df])
        Bd_idx += factor

    merged_df.reset_index(inplace=True)
    merged_df.drop('index', axis=1, inplace=True)
    merged_df.drop(merged_df[merged_df['FLAG1']==1].index, axis=0, inplace=True)

    return merged_df

    

Bd_cdf = pycdf.CDF('dscovr_h0_mag_20220101_v01.cdf')
Bd = build_day_BD(Bd_cdf)

wind_ion_cdf = pycdf.CDF('wi_h1_swe_20220101_v01.cdf')
wind_ion = build_day_WI(wind_ion_cdf)

print(merge_DFs(Bd, wind_ion))