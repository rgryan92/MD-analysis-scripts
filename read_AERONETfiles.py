# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:36:05 2017

@author: rgryan

FILE TO READ IN AND UNDERSTAND AERONET AEROSOL DATA FROM CANBERRA
"""
import pandas as pd
#%%

filepath = '/Users/rgryan/Google Drive/Documents/PhD/Data/AERONET_Canberra_March2017/20170301_20170331_Canberra'

# for angstrom exponent
# =====================
ang_path = '~/Google Drive/Documents/PhD/Data/AERONET_Canberra_March2017/030101_171231_Canberra (2)/'
ang_file = '030101_171231_Canberra.lev20'
ang_df = pd.read_csv(ang_path+ang_file, sep=',', header=4,
                     parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']])
                     
ang_df_dti = ang_df.set_index(pd.DatetimeIndex(ang_df['Date(dd-mm-yy)_Time(hh:mm:ss)']))
ang_exp_monthly = ang_df_dti['340-440Angstrom'].resample('M').mean()

#%%
ang_exp_febr = ang_exp_monthly.loc[ang_exp_monthly.index.month==2]
ang_exp_febr_mean = ang_exp_febr.mean()
ang_exp_febr_std = ang_exp_febr.std()
ang_exp_march = ang_exp_monthly.loc[ang_exp_monthly.index.month==3]
ang_exp_march_mean = ang_exp_march.mean()
ang_exp_march_std = ang_exp_march.std()
ang_exp_april = ang_exp_monthly.loc[ang_exp_monthly.index.month==4]
ang_exp_april_mean = ang_exp_april.mean()
ang_exp_april_std = ang_exp_april.std()

ang_exp_overall_mean = (ang_exp_april_mean+ang_exp_march_mean+ang_exp_febr_mean)/3
ang_exp_overall_std = (ang_exp_april_std+ang_exp_march_std+ang_exp_febr_std)/3
#%%
aem = ang_exp_febr.plot(color='red')
ang_exp_march.plot(ax=aem, color='blue')
ang_exp_april.plot(ax=aem,color='orange')
#%%
asy_path = '~/Google Drive/Documents/PhD/Data/AERONET_Canberra_March2017/030101_171231_Canberra/030101_171231_Canberra.asy'
asy_df = pd.read_csv(asy_path, sep=',', header=3,
                     parse_dates=[['Date(dd-mm-yyyy)','Time(hh:mm:ss)']])
asy_df_dti = asy_df.set_index(pd.DatetimeIndex(asy_df['Date(dd-mm-yyyy)_Time(hh:mm:ss)']))
asy_exp_monthly = asy_df_dti.resample('M').mean()
#%%
asy_440_mean = asy_exp_monthly['ASYM440-T'].mean()
asy_440_std = asy_exp_monthly['ASYM440-T'].std()
asy_676_mean = asy_exp_monthly['ASYM676-T'].mean()
asy_676_std = asy_exp_monthly['ASYM676-T'].std()
asy_870_mean = asy_exp_monthly['ASYM870-T'].mean()
asy_870_std = asy_exp_monthly['ASYM870-T'].std()
asy_1020_mean = asy_exp_monthly['ASYM1020-T'].mean()
asy_1020_std = asy_exp_monthly['ASYM1020-T'].std()

asyp = asy_exp_monthly['ASYM440-T'].plot(color='blue')
asy_exp_monthly['ASYM676-T'].plot(ax=asyp, color='red')
asy_exp_monthly['ASYM870-T'].plot(ax=asyp, color='green')
asy_exp_monthly['ASYM1020-T'].plot(ax=asyp, color='orange')

#%%
# For Single scattering albedo

ssa_path = '~/Google Drive/Documents/PhD/Data/AERONET_Canberra_March2017/030101_171231_Canberra (3)/030101_171231_Canberra.ssa'
ssa_df = pd.read_csv(ssa_path, sep=',', header=3,
                     parse_dates=[['Date(dd-mm-yyyy)','Time(hh:mm:ss)']])
ssa_df_dti = ssa_df.set_index(pd.DatetimeIndex(ssa_df['Date(dd-mm-yyyy)_Time(hh:mm:ss)']))
ssa_exp_monthly = ssa_df_dti.resample('M').mean()
#%%
ssa_440_mean = ssa_exp_monthly['SSA440-T'].mean()
ssa_440_std = ssa_exp_monthly['SSA440-T'].std()
ssa_676_mean = ssa_exp_monthly['SSA676-T'].mean()
ssa_676_std = ssa_exp_monthly['SSA676-T'].std()
ssa_870_mean = ssa_exp_monthly['SSA870-T'].mean()
ssa_870_std = ssa_exp_monthly['SSA870-T'].std()
ssa_1020_mean = ssa_exp_monthly['SSA1020-T'].mean()
ssa_1020_std = ssa_exp_monthly['SSA1020-T'].std()

ssap = ssa_exp_monthly['SSA440-T'].plot(color='blue')
ssa_exp_monthly['SSA676-T'].plot(ax=ssap, color='red')
ssa_exp_monthly['SSA870-T'].plot(ax=ssap, color='green')
ssa_exp_monthly['SSA1020-T'].plot(ax=ssap, color='orange')

#%%
aodd_path = 'C:/Users/rgryan/Google Drive/Documents/PhD/Data/AERONET_Canberra_March2017/AOD files_dailyaverages/'
canfile = '030101_171231_Canberra.lev20'
colfile = '010101_031231_Coleambally.lev20'
adefile = '060101_091231_Adelaide_Site_7.lev20'
brifile = '100101_151231_Brisbane-Uni_of_QLD.lev20'
tinfile = '980101_121231_Tinga_Tingana.lev20'
fowfile = '130101_171231_Fowlers_Gap.lev20'

candf = pd.read_csv(aodd_path+canfile, sep=',', header=4,
                     parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']], dayfirst=True)
candf = candf.set_index(pd.DatetimeIndex(candf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
candf_monthly = candf.resample('M').mean()

coldf = pd.read_csv(aodd_path+colfile, sep=',', header=4,
                     parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']])
coldf = coldf.set_index(pd.DatetimeIndex(coldf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
coldf_monthly = coldf.resample('M').mean()

adedf = pd.read_csv(aodd_path+adefile, sep=',', header=4,
                    parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']], dayfirst=True)
adedf = adedf.set_index(pd.DatetimeIndex(adedf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
adedf_monthly = adedf.resample('M').mean()

fowdf = pd.read_csv(aodd_path+fowfile, sep=',', header=4,
                    parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']], dayfirst=True)
fowdf = fowdf.set_index(pd.DatetimeIndex(fowdf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
fowdf_monthly = fowdf.resample('M').mean()

bridf = pd.read_csv(aodd_path+brifile, sep=',', header=4,
                    parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']], dayfirst=True)
bridf = bridf.set_index(pd.DatetimeIndex(bridf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
bridf_monthly = bridf.resample('M').mean()

tindf = pd.read_csv(aodd_path+tinfile, sep=',', header=4,
                    parse_dates=[['Date(dd-mm-yy)','Time(hh:mm:ss)']], dayfirst=True)
tindf = tindf.set_index(pd.DatetimeIndex(tindf['Date(dd-mm-yy)_Time(hh:mm:ss)']))
tindf_monthly = tindf.resample('M').mean()

#%%
aodplot = candf_monthly['AOT_440'].plot(figsize=(10,2), color='blue')
coldf_monthly['AOT_440'].plot(ax=aodplot, color='purple')
adedf_monthly['AOT_440'].plot(ax=aodplot, color='red')
bridf_monthly['AOT_440'].plot(ax=aodplot, color='grey')
tindf_monthly['AOT_440'].plot(ax=aodplot, color='orange')
fowdf_monthly['AOT_440'].plot(ax=aodplot, color='green')

aodplot.legend(['Canberra', 'Coleambally', 'Adelaide', 'Brisbane', 'Tingana', 
                'Fowlers Gap'], loc=2, bbox_to_anchor=(1,1))
f = aodplot.get_figure()
f.savefig(aodd_path+'AOD_avgs_SE_Australia.png', bbox_inches='tight')
