from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'), 
	url(r'^outil/(\d+)$', views.outil, name = 'outil'),
	url(r'^ouvrier/(\d+)$', views.ouvrier, name='ouvrier'), 

]