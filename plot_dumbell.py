#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 19:45:17 2022

@author: zhiming
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns
import re


def read_iperf(filename):
    bandwith = []
    cwnd = []
    rtt = []
    with open(filename) as fp_in:
        for i, line in enumerate(fp_in):
            if i >= 7:
                try:
                    
                    bandwith.append(float(re.findall(r"\d+", line.split('  ')[3])[0]))
                except:
                    bandwith.append(line.split(' ')[9])
                cwnd.append(int(line.split(' ')[-4].split('/')[0][0:-1]))
                rtt.append(int(line.split(' ')[-4].split('/')[1])/1000)
    bandwith.pop(-1)
    cwnd.pop(-1)
    rtt.pop(-1)
    dic = {'throughput': bandwith, 'cwnd':cwnd, 'rtt':rtt}
    return pd.DataFrame(dic)


################################### Scenario 1 #########################
dfccp1 = read_iperf('./logs/ccp1.log')
dfccp2 = read_iperf('./logs/ccp2.log')
dfbbr1 = read_iperf('./logs/bbr1.log')
dfbbr2 = read_iperf('./logs/bbr2.log')
dfcubic1 = read_iperf('./logs/cubic1.log')
dfcubic2 = read_iperf('./logs/cubic2.log')
#sns.set('whitegrid')

###################Throughput  1################################
#############plot for h1
fig, ax = plt.subplots()
ax.plot(dfccp1['throughput'].ewm(com=10).mean(), '-', label = 'LUC')
ax.plot(dfbbr1['throughput'].ewm(com=10).mean(), '-.', label = 'BBR')
ax.plot(dfcubic1['throughput'].ewm(com=10).mean(), '--', label = 'CUBIC')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Throughput (Mbps)')
ax.grid(True)
ax.legend()
fig.savefig('./results/homoflow_thru_h1.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
############plot for h2
fig, ax = plt.subplots()
ax.plot(dfccp2['throughput'].ewm(com=10).mean(), '-',  label = 'LUC')
ax.plot(dfbbr2['throughput'].ewm(com=10).mean(), '-.', label = 'BBR')
ax.plot(dfcubic2['throughput'].ewm(com=10).mean(), '--', label = 'CUBIC')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Throughput (Mbps)')
ax.grid(True)
ax.legend()
fig.savefig('./results/homoflow_thru_h2.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)


################### RTT  1 ################################
#############plot for h1
fig, ax = plt.subplots()
ax.plot(dfccp1['rtt'].ewm(com=10).mean(), '-', label = 'LUC')
ax.plot(dfbbr1['rtt'].ewm(com=10).mean(), '-.', label = 'BBR')
ax.plot(dfcubic1['rtt'].ewm(com=10).mean(), '--', label = 'CUBIC')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('RTT (ms)')
ax.grid(True)
ax.legend()
fig.savefig('./results/homoflow_rtt_h1.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
############plot for h2
fig, ax = plt.subplots()
ax.plot(dfccp2['rtt'].ewm(com=10).mean(), '-',  label = 'LUC')
ax.plot(dfbbr2['rtt'].ewm(com=10).mean(), '-.', label = 'BBR')
ax.plot(dfcubic2['rtt'].ewm(com=10).mean(), '--', label = 'CUBIC')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('RTT (ms)')
ax.grid(True)
ax.legend()
fig.savefig('./results/homoflow_rtt_h2.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)

################################### Scenario 2 #########################
dfccp1bbr2 = read_iperf('./logs/ccp1bbr2.log')
dfbbr2ccp1 = read_iperf('./logs/bbr2ccp1.log')
dfccp1cubic2 = read_iperf('./logs/ccp1cubic2.log')
dfcubic2ccp1 = read_iperf('./logs/cubic2ccp1.log')
dfbbr1cubic2 = read_iperf('./logs/bbr1cubic2.log')
dfcubic2bbr1 = read_iperf('./logs/cubic2bbr1.log')

###################Throughput  2################################
#############plot for ccp and bbr ######
fig, ax = plt.subplots()
ax.plot(dfccp1bbr2['throughput'].ewm(com=10).mean(), '-', label = 'h1 (LUC)')
ax.plot(dfbbr2ccp1['throughput'].ewm(com=10).mean(), '-.', label = 'h2 (BBR)')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Throughput (Mbps)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_thru_ccpbbr.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for ccp and cubic ######
fig, ax = plt.subplots()
ax.plot(dfccp1cubic2['throughput'].ewm(com=10).mean(), '-', label = 'h1 (LUC)', color = 'tab:blue')
ax.plot(dfcubic2ccp1['throughput'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Throughput (Mbps)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_thru_ccpcubic.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for ccp and cubic ######
fig, ax = plt.subplots()
ax.plot(dfbbr1cubic2['throughput'].ewm(com=10).mean(), '-.', label = 'h1 (BBR)',  color = 'tab:orange')
ax.plot(dfcubic2bbr1['throughput'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('Throughput (Mbps)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_thru_bbrcubic.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)


###################RTT  2################################
#############plot for ccp and bbr ######
fig, ax = plt.subplots()
ax.plot(dfccp1bbr2['rtt'].ewm(com=10).mean(), '-', label = 'h1 (LUC)')
ax.plot(dfbbr2ccp1['rtt'].ewm(com=10).mean(), '-.', label = 'h2 (BBR)')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('RTT (ms)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_rtt_ccpbbr.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for ccp and cubic ######
fig, ax = plt.subplots()
ax.plot(dfccp1cubic2['rtt'].ewm(com=10).mean(), '-', label = 'h1 (LUC)', color = 'tab:blue')
ax.plot(dfcubic2ccp1['rtt'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('RTT (ms)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_rtt_ccpcubic.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
    
#############plot for ccp and cubic ######
fig, ax = plt.subplots()
ax.plot(dfbbr1cubic2['rtt'].ewm(com=10).mean(), '-.', label = 'h1 (BBR)',  color = 'tab:orange')
ax.plot(dfcubic2bbr1['rtt'].ewm(com=10).mean(), '--', label = 'h2 (CUBIC)', color ='tab:green')
ax.set_xlabel('Duration (s)')
ax.set_ylabel('RTT (ms)')
ax.grid(True)
ax.legend()
fig.savefig('./results/heteflow_rtt_bbrcubic.eps', format='eps', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)