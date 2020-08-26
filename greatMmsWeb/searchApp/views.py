from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
import json
import os
from django import forms



def index(request):
    template = loader.get_template('searchApp/index.html')
    context = {
        'latest_question_list': 1,
    }
    return HttpResponse(template.render(context, request))

def fetchReport(request, date_input):
	print("datereceived", date_input)
	file_to_fetch = "csv/SITL-{}.csv".format(date_input)
	print(os.path.join(settings.BASE_DIR, file_to_fetch), "BASED")
	data = None
	try:
		with open(file_to_fetch, mode='r') as fileIn:
			data = {}
			data['header'] = fileIn.readline().strip("\n")
			data_body = fileIn.readlines()
			# remove "/n from data_body":
			for row in data_body:
				row.strip("\\")
			data['body'] = data_body

	except Exception as e:
		print("File not available.", e)
		raise Http404("Data not available")
	context = {'sitl_report': data }
	if context['sitl_report'] == None:
		print("No data to send")
	else:
		print("DATa", data)
		return HttpResponse(json.dumps(context))
