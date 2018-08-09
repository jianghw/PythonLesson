from django.conf.urls import url

from polls import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex /polls/4/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex /polls/4/result
    url(r'^(?P<question_id>[0-9]+)/result/$', views.result, name='result'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
