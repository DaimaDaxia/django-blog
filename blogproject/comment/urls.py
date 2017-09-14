from django.conf.urls import url

from . import views

app_name = 'comment'

urlpatterns = [
    url('^comment/post/(?P<post_pk>\d+)$', views.post_comment, name='comments'),

]