from django.shortcuts import render
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Course
from .forms import CourseForm
from django.http import HttpResponseRedirect



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def add_course(request):
    template = "add_course.html"

    if request.method == "POST":
        
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse_lazy('users:index'))
    else:
        context = {
            'course_form': CourseForm(),
        }
    return render(request, template, context)