from django.conf.urls import url
from . import views

app_name = 'database'
urlpatterns = [
    url(r'^$', views.db_list, name='db_list'),
    url(r'^upload/$', views.db_upload, name='db_upload'),
    url(r'^download/(?P<file_id>[0-9]+)/$', views.db_download, name='db_download'),
]
