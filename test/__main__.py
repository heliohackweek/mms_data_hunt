#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
This runs the necessary tests to check one's Python environment for the mms_data_hunt Python package.
'''
import os
import sys
import subprocess as sub

if __name__ == '__main__':
    # check Python version
    print('You are currently running Python ' + '.'.join(map(str,sys.version_info)))
    if sys.version_info[0] < 3:
        print('Please ensure you are running Python 3.x series from the Miniconda/Anaconda distribution.')
        sys.exit()

    # check Git repo (can I do this on Windows?)
    #try:
    #    branch = sub.Popen(['git', 'branch'], stderr=sub.STDOUT, stdout=sub.STDOUT) #, stdout=open(os.devnull, 'w'))
    #    print(branch)
    #except Exception as e:
    #    print('Failed Git repo check.')
    #    print(e)
    #    sys.exit()
    #if branch:
    #if sub.call(["git", "branch"], stderr=sub.STDOUT, stdout=open(os.devnull, 'w')) != 0:
    #    print('You are currently on the ' + branch + ' of the Git repository.')
    #else:
    #    print('Please ensure you have cloned the GitHub repository here: \n'
    #          + '\thttps://github.com/heliohackweek/mms_data_hunt\n'
    #          + 'and then try the test script again.')
    #    sys.exit()

    # check imports
else:
    print('This module was meant to run as an executable script. '
          + 'Please use "python /path/to/test" instead of using import')
