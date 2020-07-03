from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.home, name='home'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'login/$', views.login, name = 'login'),
    url(r'dashboard/$', views.dashboard, name = 'dashboard'),
    url(r'surveyquestion/(?P<pk>\d+)/$', views.ques, name = 'ques'),
    url(r'submit/(?P<pk>\d+)/$', views.submit, name = 'submit'),
    url(r'response/$', views.response, name = 'response'),
    url(r'edit/(?P<pk>\d+)/$', views.edit, name = 'edit'),
    url(r'report/(?P<pk>\d+)/$', views.report, name = 'report'),
]