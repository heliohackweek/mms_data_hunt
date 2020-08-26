#import modules
from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='index'),
	path('date/<str:date_input>', views.fetchReport, name='fetchReport'),
]
