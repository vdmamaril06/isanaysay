from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    url(r'^add_course$', add_course, name='add-course'),
    url(r'^add_essay$', add_essay, name='add-essay'),
    url(r'^view_essay/(?P<essay_id>\d+)$', view_essay, name='view-essay'),
]