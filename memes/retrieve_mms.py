#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
##############################################################################
This utility reads MMS data files into NumPy arrays.
##############################################################################
'''

import os
from datetime import datetime, timedelta
import glob
import numpy as np

import cdflib

def get_fgm(basepath, starttime, endtime, mms_sat='1'):
        """Reads magnetic data from FGM instrument that has been saved locally.

        Parameters
        ==========
        basepath :  str
                                Path to data, which is stored under year/month/daily_file.cdf.
        starttime : datetime.datetime object
                                Start time of data to be read
        endtime :   datetime.datetime object
                                End time of data to be read
        mms_sat :       str (optional, default='1')
                                Satellite number to use.

        Returns
        =======
        (t, Bt, Bx, By, Bz) - tuple of numpy arrays
        """

        n_days = int(np.ceil((endtime - starttime).total_seconds()/60./60./24.))
        day_list = [starttime + timedelta(days=n) for n in range(n_days)]

        t_utc, B_x, B_y, B_z, Bt = [], [], [], [], []

        for day in day_list:
            year, month = starttime.strftime('%Y'), starttime.strftime('%m')
            str_date_event = starttime.strftime('%Y%m%d')
            test_path = os.path.join(basepath, year, month,
                                    'mms{}_fgm_srvy_l2_{}_*'.format(mms_sat, str_date_event))
            cdf_path = glob.glob(test_path)

            if len(cdf_path) == 0:
                raise Exception("File ({}) does not exist! Make sure to download it!".
                    format(test_path))
            else:
                read_cdf_path = cdf_path[0]

            print("Reading file at", read_cdf_path)

            # CDF read:
            mms_data = cdflib.CDF(read_cdf_path)
            mag_data = mms_data.varget('mms{}_fgm_b_gse_srvy_l2'.format(mms_sat)) # changed to use GSE coords

            # Extract data:
            B_x.append(mag_data[:,0])
            B_y.append(mag_data[:,1])
            B_z.append(mag_data[:,2])
            Bt.append(mag_data[:,3])

            t_utc_ = np.array([datetime.utcfromtimestamp(x) for x in cdflib.cdfepoch.unixtime(mms_data['Epoch'][...])])
            t_utc.append(t_utc_)

        # Pack into arrays:
        B_x = np.concatenate(B_x)
        B_y = np.concatenate(B_y)
        B_z = np.concatenate(B_z)
        Bt = np.concatenate(Bt)
        t_utc = np.concatenate(t_utc)

        # Cut to time range:
        cut_inds = np.where(np.logical_and(t_utc >= starttime, t_utc < endtime))

        return (t_utc[cut_inds], B_x[cut_inds], B_y[cut_inds], B_z[cut_inds], Bt[cut_inds])


def get_fpi(basepath, starttime, endtime, mms_sat=1):
    """Reads Ion properties (speed and density) from FPI instrument that has been saved locally.

    Parameters
    ==========
    basepath :  str
                            Path to data, which is stored under year/month/daily_file.cdf.
    starttime : datetime.datetime object
                            Start time of data to be read
    endtime :   datetime.datetime object
                            End time of data to be read
    mms_sat :       str (optional, default='1')
                            Satellite number to use.

    Returns
    =======
    (t, speed_x, speed_y, speed_z, density) - tuple of numpy arrays
    """

    n_days = int(np.ceil((endtime - starttime).total_seconds()/60./60./24.))
    day_list = [starttime + timedelta(days=n) for n in range(n_days)]

    speed_x, speed_y, speed_z = [], [], []
    t_utc, density = [], [] # technically, t_utc should be same in both var arrays

    for day in day_list:
        year, month = starttime.strftime('%Y'), starttime.strftime('%m')
        str_date_event = starttime.strftime('%Y%m%d')
        # ISSUE: we have cdf files at hour specifications (retruns 1+ files)
        test_path = os.path.join(basepath, year, month,
                                'mms{}_fpi_fast_l2_dis-moms_{}*0000_*'.format(mms_sat, str_date_event))
        cdf_path = glob.glob(test_path)

        if len(cdf_path) == 0:
            raise Exception("File ({}) does not exist! Make sure to download it!".format(test_path))
        #else:
        #    read_cdf_path = cdf_path[0]

        for read_cdf_path in cdf_path:
            print("Reading file at", read_cdf_path)
            # CDF read:
            mms_data = cdflib.CDF(read_cdf_path)

            v = mms_data.varget('mms{}_dis_bulkv_gse_fast'.format(mms_sat))
            p = mms_data.varget('mms{}_dis_numberdensity_fast'.format(mms_sat))

            # Extract data:
            speed_x.append(v[:,0])
            speed_y.append(v[:,1])
            speed_z.append(v[:,2])
            
            density.append(p)

        t_utc_ = np.array([datetime.utcfromtimestamp(x) for x in cdflib.cdfepoch.unixtime(mms_data['Epoch'][...])])
        t_utc.append(t_utc_)

    # Pack into arrays:
    speed_x = np.concatenate(speed_x)
    speed_y = np.concatenate(speed_y)
    speed_z = np.concatenate(speed_z)
    density = np.concatenate(density)
    t_utc = np.concatenate(t_utc)

    # Cut to time range:
    cut_inds = np.where(np.logical_and(t_utc >= starttime, t_utc < endtime))

    return (t_utc[cut_inds], speed_x[cut_inds], speed_y[cut_inds], speed_z[cut_inds], density[cut_inds])
    print("Not implemented.")
