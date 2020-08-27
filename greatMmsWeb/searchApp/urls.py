#import modules
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('sitl_reports/', views.reportUI, name='reportUserInterface'),
]
