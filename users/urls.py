from django.urls import path
from .views import *
from django.contrib.auth import views
from django.conf.urls import url
from django.urls import reverse_lazy

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password/change/', views.PasswordChangeView.as_view(template_name='password_change.html',success_url=reverse_lazy('home')), name='password-change'),
    path('login/',views.LoginView.as_view(template_name="registration/login.html",authentication_form=UserLoginForm),name='login'),
    url(r'^view_courses$', view_courses, name='view-courses'),
    url(r'^add_course$', add_course, name='add-course'),
    url(r'^update_course/(?P<course_id>\d+)$', update_course, name='update-course'),
    url(r'^delete_course/(?P<course_id>\d+)$', delete_course, name='delete-course'),
    url(r'^view_essays$', view_essays, name='view-essays'),
    url(r'^add_essay$', add_essay, name='add-essay'),
    url(r'^update_essay/(?P<essay_id>\d+)$', update_essay, name='update-essay'),
    url(r'^delete_essay/(?P<essay_id>\d+)$', delete_essay, name='delete-essay'),
    url(r'^view_essay/(?P<essay_id>\d+)$', view_essay, name='view-essay'),
    url(r'^view_essay_submissions$', view_essay_submissions, name='view-essay-submissions'),
    url(r'^add_essay_submission/(?P<essay_id>\d+)$', add_essay_submission, name='add-essay-submission'),
    url(r'^update_essay_submission/(?P<essay_submission_id>\d+)$', update_essay_submission, name='update-essay-submission'),
    url(r'^delete_essay_submission/(?P<essay_submission_id>\d+)$', delete_essay_submission, name='delete-essay-submission'),
    url(r'^view_essay_submission/(?P<essay_submission_id>\d+)$', view_essay_submission, name='view-essay-submission'),
    url(r'^update_profile/(?P<user_id>\d+)$', update_profile, name='update-profile'),
    url(r'^view_essay_submissions_for_teacher$', view_essay_submissions_for_teacher, name='view-essay-submissions-for-teacher'),
    url(r'^view_essay_submission_for_checking/(?P<essay_submission_id>\d+)$', view_essay_submission_for_checking, name='view-essay-submission-for-checking'),
]