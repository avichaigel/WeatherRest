from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/forecast$', views.new_forecast),
    url(r'^api/login$', views.login),
    url(r'^api/register$', views.register)
]