from django import forms
import datetime

class DateForm(forms.Form):
    date_field = forms.DateField(label='Date', required=False)
    search_event_type = forms.CharField(label='Event type', max_length=400, required=False)
    last_n_events_type = forms.CharField(label='Event type', max_length=400, required=False)
    last_n_events_num = forms.IntegerField(label='# of events', required=False)