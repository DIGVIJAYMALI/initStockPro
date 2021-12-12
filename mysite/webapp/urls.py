from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),   #homepage setup
	url(r'^GetStockAnalysisCSV/', views.GetStockAnalysisCSV, name="GetStockAnalysisCSV"),
url(r'^GetStockAnalysisData/', views.GetStockAnalysisData, name="GetStockAnalysisData"),
]
