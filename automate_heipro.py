# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:29:27 2017

@author: rgryan
"""
import subprocess
import os
filenumbers = [1, 2]

#sp.call(['ls', '-l', 'C:/Sciatran2/AEROSOL_RETRIEVAL_v-1-5/IDL_execute/aerosol_retrieval.inp'])
#time = subprocess.Popen('date', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#output, err= time.communicate()
#print('it is'+str(output))


os.system('cd C:/RSI/IDL63/bin/bin.x86_64/')
os.system('idlrt.exe -vm=C:/Sciatran2/AEROSOL_RETRIEVAL_v-1-5/IDL_execute/aerosol_retrieval.sav')