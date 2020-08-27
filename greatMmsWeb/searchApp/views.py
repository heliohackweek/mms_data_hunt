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
        if form.is_valid():
            date_value = request.POST['date_field']
            context['date'] = datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
            # return HttpResponse("Thanks")
            retreived_data = fetch_data_from_csv(date_value)
            if retreived_data['header'] == None and retreived_data['body'] == None:
                context['sitl_report'] = None
            else:
                context['sitl_report'] = retreived_data
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DateForm()
        context['form'] = form
        context['sitl_report'] = "initial"
        print('Else executed')
    return render(request, 'searchApp/sitl_report_ui.html', context)

def fetch_data_from_csv(date_to_search):
    '''
    func to fetch data from the csv based on date provided
    input: date to search (date_to_search)
    output: dictionary of data
    '''
    print("datereceived", date_to_search)
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
