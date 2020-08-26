#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
##############################################################################
This utility parses the Berkely SITL report page for reports and retrieves
the ASCII text to be parsed.
##############################################################################
'''
import requests
import pandas as pd
import numpy as np

base_url = 'http://www.ssl.berkeley.edu/~moka/eva'

records = [
    'sitl_report.json',
    'sitl_report_2018-2019.json',
    'sitl_report_2015-2017.json',
]

def get():
    '''could expand this to be dependent upon date requested'''

    reports = []

    # read in json file
    for r in records:
        r = requests.get(base_url + '/' + r)

        # report urls identified from web page source code
        for record in r.json():
            report = base_url + '/list/' + record['YYYY'] + '/' + record['PNAME'] + '.txt'
            reports.append(report)

    # parse reports ascii to Pandas DF (from project demo)
    keys = ['datetime', 'FOM', 'ID', 'Discussion']

    reports_pds = []
    for report in reports:
        try:
            r = requests.get(report)
            data = r.text.splitlines()[15:-1] #ignore header info and trailing line

            rows = []
            for line in data:
                rows.append(dict(zip(keys, line.split(',', 3))))
            reports_pds.append(pd.DataFrame(rows[1:]))    # [1:] to skip column names
        except Exception as e:
            print(e)
            print('Issue with processing this report:')
            print(report)

    # Combine lists into single DataFrame:
    reports_df = pd.concat(reports_pds)
    # Sort by date:
    reports_df = reports_df.sort_values(by='datetime')
    # Use monotonically increasing index:
    reports_df = reports_df.reset_index(drop=True)

    return reports_df


def parse_times(reports_df):
    """Parses start time and end times into datetime objects for easier handling."""

    # Split the time column into start time and end time:
    reports_df[['Starttime','Endtime']] = reports_df['datetime'].str.split(" - ", expand=True)

    ## Parse the time columns into datetime objects:
    tformat_sitl = '%Y-%m-%d/%H:%M:%S'
    reports_df['Starttime'] = pd.to_datetime(reports_df['Starttime'], format=tformat_sitl)
    reports_df['Endtime'] = pd.to_datetime(reports_df['Endtime'], format=tformat_sitl)

    return reports_df


def combine_rows(reports_df):
    """Combines rows with identical discussions descriptions so that starttime and
    endtime match the first and last discussions."""

    # Add the colum 'Day' just in case strings repeat themselves over the whole dataset
    # under the assumption you won't find identical ones in the same day for different events
    day = [np.datetime_as_string(d, unit='D') for d in reports_df.Starttime.to_numpy()]
    reports_df['Day'] = day
    # Find first and last in list of duplicate reports:
    first_reports = reports_df.duplicated(subset=['Discussion', 'Day'], keep='first').to_numpy()
    last_reports = reports_df.duplicated(subset=['Discussion', 'Day'], keep='last').to_numpy()
    # Find the points that are in between those:
    mid_dupl = first_reports == last_reports
    duplicates = np.where(np.logical_and(first_reports == True, mid_dupl == True))[0]
    # Drop those reports between first and last:
    reduced_df = reports_df.drop(duplicates)
    # Reset index after losing rows:
    reduced_df = reduced_df.reset_index(drop=True)

    # Now find duplicates again but take the end time into the original record:
    first_reports = reduced_df.duplicated(subset=['Discussion', 'Day'], keep='last').to_numpy()
    replace_endtime = np.where(first_reports == True)[0]
    for i in replace_endtime:
        reduced_df.at[i, 'Endtime'] = reduced_df['Endtime'][i+1]
    reduced_df = reduced_df.drop_duplicates(subset=['Discussion', 'Day'], keep='first')

    # And reset index again:
    reduced_df = reduced_df.reset_index(drop=True)

    return reduced_df


if __name__ == '__main__':
    print(get())
