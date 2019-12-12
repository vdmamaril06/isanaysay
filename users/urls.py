from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    url(r'^view_courses$', view_courses, name='view-courses'),
    url(r'^add_course$', add_course, name='add-course'),
    url(r'^update_course/(?P<course_id>\d+)$', update_course, name='update-course'),
    url(r'^delete_course/(?P<course_id>\d+)$', delete_course, name='delete-course'),
    url(r'^view_essays$', view_essays, name='view-essays'),
    url(r'^add_essay$', add_essay, name='add-essay'),
    url(r'^update_essay/(?P<essay_id>\d+)$', update_essay, name='update-essay'),
    url(r'^delete_essay/(?P<essay_id>\d+)$', delete_essay, name='delete-essay'),
    url(r'^view_essay/(?P<essay_id>\d+)$', view_essay, name='view-essay'),
    url(r'^add_word$', add_word, name='add-word'),
]