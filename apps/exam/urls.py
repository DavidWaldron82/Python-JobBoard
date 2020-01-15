from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^new_job$', views.new_job),
    url(r'^create_job$', views.create_job),
    url(r'^remove/(?P<job_id>\d+)$', views.remove_job),
    url(r'^edit_job/(?P<job_id>\d+)$', views.edit_job),
    url(r'^update/(?P<job_id>\d+)$', views.update_job),
    url(r'^show_job/(?P<job_id>\d+)$', views.show_job),
    url(r'^logout$',views.logout),
]