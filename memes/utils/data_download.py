#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
##############################################################################
This utility downloads data and SITL reports from MMS mission.

Could be built into an interactive CLI to specify MMS instrument, probe,
and user-defined datetime.
##############################################################################
'''
import pandas as pd
import pyspedas
import datetime as dt
import multiprocessing
import itertools

# download only data, not plot
pyspedas.mms.mms_config.CONFIG['download_only'] = True

def get_data(args):
    t_range, probes = args
    print(t_range, probes)

    fgm_vars = pyspedas.mms.fgm(
        trange       = t_range,
        time_clip    =   False, # could truncate residuals at trange ends
        data_rate    =  'srvy', # survey frequency
        level        =    'l2', # ensure L2 products
        probe        =  probes, # all 4 MMS spacecraft
    )

    # Speed & Density data (GSE and GSM coords) for FPI instrument
    fpi_vars = pyspedas.mms.fpi(
        trange       =    t_range,
        time_clip    =      False, # could truncate residuals at trange ends
        data_rate    =     'fast', # fast frequency
        level        =       'l2', # ensure L2 products
        probe        =     probes, # all 4 MMS spacecraft
        datatype     = 'dis-moms', # CDF filename conventions (dis  -> Dual Ion Spectrometer)
                                   #                          (moms -> moments)
    )

if __name__ == '__main__':
    t = [('2020-01-01', '2020-07-16'), # latest 6-months of observations
         ('2016-06-01', '2016-12-31')] # data used in article
    probes = ['1', '2', '3', '4']

    # get all dates
    dates = []
    for sdate, edate in t:
        s = dt.datetime.strptime(sdate, '%Y-%m-%d')
        e = dt.datetime.strptime(edate, '%Y-%m-%d')
        dates.append(pd.date_range(s,e-dt.timedelta(days=1),freq='d'))
    dates = dates[0].union(dates[1])

    args = []
    for d, p in list(itertools.product(dates, probes)):
        args.append((
            (d.strftime('%Y-%m-%d'), (d+dt.timedelta(days=1)).strftime('%Y-%m-%d')),
            p
        ))

    p = multiprocessing.Pool(12)
    p.map(get_data, args)
