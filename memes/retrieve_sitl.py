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

base_url = 'http://www.ssl.berkeley.edu/~moka/eva'

records = [
    'sitl_report.json',
    'sitl_report_2018-2019.json',
    'sitl_report_2015-2017.json',
]

def get():
    '''could expand this to be depenent upon date requested'''

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
            reports_pds.append(pd.DataFrame(rows))
        except Exception as e:
            print(e)
            print('Issue with processing this report:')
            print(report)
    return reports_pds

if __name__ == '__main__':
    print(get())
