from django import forms
import datetime

class DateForm(forms.Form):
    date_field = forms.DateField(label='Date')
