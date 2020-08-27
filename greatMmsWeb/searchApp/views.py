from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
import json
import os
from django import forms
from .forms import DateForm
import datetime
from searchApp.models import STIL_Report

def index(request):
    template = loader.get_template('searchApp/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def reportUI(request):
    context = {
        'sitl_report': ''
    }
    if request.method == 'POST':
        print('Entered post')
        form = DateForm(request.POST) 
        context['form'] = form
        btnKeys = request.POST.keys()
        # if generate button
        if "submitBtn" in btnKeys:
            date_value = request.POST['date_field']
            context['date'] = datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
            retreived_data = fetch_data_from_db(date_value)
        elif "searchBtn" in btnKeys:
            event_type = request.POST['search_event_type']
            retreived_data = query_event_type(event_type)
        elif "searchNEventsBtn" in btnKeys:
            event_type = request.POST['last_n_events_type']
            num_of_events = int(request.POST['last_n_events_num'])
            retreived_data = query_lastN_events(event_type, num_of_events)
        else:
            retreived_data['header'] = None
            retreived_data['body'] = None
        
        if retreived_data['header'] == None and retreived_data['body'] == None:
            context['sitl_report'] = None
        else:
            context['sitl_report'] = retreived_data
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DateForm()
        context['form'] = form
        context['sitl_report'] = "initial"
    return render(request, 'searchApp/sitl_report_ui.html', context)

def fetch_data_from_db(date_to_search):
    '''
    func to fetch data from the db based on date
    input: date to search (date_to_search)
    output: dictionary of data
    '''
    reports = STIL_Report.objects.all()
    date_arr = date_to_search.split('-')
    year_date_to_search = date_arr[0]
    month_date_to_search = date_arr[1]
    day_date_to_search = date_arr[-1]
    # data
    data = {'header': None, 'body': None}
    # filter
    try:
        filter_report = list(reports.filter(start_datetime_field__year=year_date_to_search, \
                start_datetime_field__month=month_date_to_search, \
                start_datetime_field__day=day_date_to_search))
    except Exception as e:
        print("No report found.", e)
    
    if len(filter_report) == 0:
        return data
    else:
        data['header'] = ['START DATE', 'END DATE', 'FOM', 'ID', 'DISCUSSION']
        data['body'] = filter_report
        return data

def query_event_type(event_type):
    '''
    func to fetch data from the db based on event type
    input: event type (dipolarization, bbf)
    output: dictionary of data
    '''
    # data
    data = {'header': None, 'body': None}
    try:
        filter_report = list(STIL_Report.objects.filter(discusson__contains=event_type))
        data['header'] = ['START DATE', 'END DATE', 'FOM', 'ID', 'DISCUSSION']
        data['body'] = filter_report
    except Exception as e:
        print("No report found.", e)

    return data

def query_lastN_events(event_type, num_of_events):
    '''
    func to fetch data from the db based on event type and it will return the first n records
    input: event type (dipolarization, bbf) and number of events
    output: dictionary of data
    ''' 
    # data
    data = {'header': None, 'body': None}
    try:
        filter_report = list(STIL_Report.objects.filter(discusson__contains=event_type)[:num_of_events])
        data['header'] = ['START DATE', 'END DATE', 'FOM', 'ID', 'DISCUSSION']
        data['body'] = filter_report
    except Exception as e:
        print("No report found.", e)

    return data

def fetch_data_from_csv(date_to_search):
    '''
    func to fetch data from the csv based on date provided
    input: date to search (date_to_search)
    output: dictionary of data
    '''
    
    file_to_fetch = "csv/SITL-{}.csv".format(date_to_search)
    data = None
    try:
        with open(file_to_fetch, mode='r') as fileIn:
            data = {'header': []}
            # file data
            file_data = fileIn.read().split("\n")
            # insert the header
            data['header'] = file_data[0].split(",")
            file_data = file_data[1:-1]
            data['body'] = []
            # insert the data for the body attribute
            for i in range(0, len(file_data)):
                temp_item_array = file_data[i].split(",")
                #some discussion strings have comma so split wont work
                temp_array_for_discussion = temp_item_array[3:]
                if len(temp_array_for_discussion) > 1:
                    temp_array_for_discussion_string = " ".join(temp_array_for_discussion)
                    # remove double quotes if any
                    temp_item_array[3] = temp_array_for_discussion_string.strip('"')
                    temp_item_array = temp_item_array[:4]
                data['body'].append(temp_item_array)
    except Exception as e:
        print("File not found.", e)
        data = {'header': None, 'body': None}
    return data



