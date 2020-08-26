#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
##############################################################################
This utility parses the Berkely SITL report page for reports and retrieves
the ASCII text to be parsed.
##############################################################################
'''
import os
import requests
import pandas as pd
from tqdm import tqdm

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
    keys = ['DATETIME', 'FOM', 'ID', 'DISCUSSION']

    reports_pds = []
    for report in reports:
        try:
            r = requests.get(report)
            #data = r.text.splitlines()[15:-1] #ignore header info and trailing line
            # index of "START"
            start_index = r.text.find("START")
            # extract data from the "START" index
            r = r.text[start_index:-1]
            # extract everything except the header info and last line
            # header inf0 --> ['START TIME - END TIME , FOM, ID, DISCUSSION']
            data = r.splitlines()[1:-1]

            rows = []
            for line in data:
                rows.append(dict(zip(keys, line.split(',', 3))))
            reports_pds.append(pd.DataFrame(rows))
        except Exception as e:
            print(e)
            print('Issue with processing this report:')
            print(report)
    return reports_pds

def create_csv(reports_df):
    """
    @function to create csv of individual records
    @input: sequence of STIL report
    @output: csv file
    """

    # create folder for all the csv files
    current_wd = os.getcwd()
    # folder to create
    output_folder_name = "csv"
    output_dir = os.path.normpath(current_wd + os.sep + output_folder_name) + "/"
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    with tqdm(total=len(reports_df)) as pbar:
        for report in reports_df:
            # file_name format: 'SITL-2016-04-05'
            if len(report.values) > 0:
                file_name = "SITL-{}.csv".format(report.iloc[0][0].split("/")[0])
                # output the file
                report.to_csv(output_dir+file_name, sep=",", index=False, header=True,encoding="utf-8")
                pbar.update(1)

    # create csv of all the dataset combined
    df = pd.DataFrame()
    for report in reports_df:
        if(len(report.values) > 0):
            df = pd.concat([df, report])
    # export it
    combined_csv_file_name = "Combined_SITL_REPORTS.csv"
    df.to_csv(output_dir+combined_csv_file_name, sep=",", index=False, header=True,encoding="utf-8")


if __name__ == '__main__':
#    print(get())
    fetched_data = get()
    # generate csv
    create_csv(fetched_data)
