from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from spellchecker import SpellChecker
from collections import Counter
from django.db.models.query import QuerySet
from django.db.models import Count
import datetime
import spacy
nlp = spacy.load('en_core_web_sm')

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def add_course(request):    
    template = "add_course.html"
    user_id = request.user.id
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            """
            c = Course.objects.order_by('-id')[0]
            t = CustomUser.objects.get(id=request.user.id)
            assignment_x = Assignment(course=c,teacher=t)
            assignment_x.save()
            """
            return HttpResponseRedirect(reverse_lazy('view-courses'))
    else:
        context = {
            'course_form': CourseForm(initial={'teacher': user_id}),
        }
    return render(request, template, context)

def delete_course(request, course_id):
    course = Course.objects.get(id=int(course_id))
    course.delete()
    return HttpResponseRedirect(reverse_lazy('view-courses'))

def update_course(request, course_id):
    template = "update_course.html"
    user_id = request.user.id
    course = Course.objects.get(id=int(course_id))
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            context = {
                'course_form': CourseForm(instance=course,initial={'teacher': user_id}),
            }
    else:
        context = {
            'course_form': CourseForm(instance=course,initial={'teacher': user_id}),
        }
    return render(request, template, context)

def view_courses(request):
    user_id = request.user.id
    template = "list_course.html"
    #course_school_years = Course.objects.values('course_school_year').annotate(dcount=Count('course_school_year'))
    course_school_years = Course.objects.select_related('teacher').filter(teacher__id=user_id).values('course_school_year').annotate(dcount=Count('course_school_year'))
    course_semesters = Course.objects.select_related('teacher').filter(teacher__id=user_id).values('course_semester').annotate(dcount=Count('course_semester'))
    courses = Course.objects.select_related('teacher').filter(teacher__id=user_id)
    context = {
        'course_school_years': course_school_years,
        'course_semesters': course_semesters,
        'courses': courses,
        'user_id': user_id,
    }
    return render(request, template, context)

def add_essay(request):
    template = "add_essay.html"

    if request.method == "POST":
        
        form = EssayForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse_lazy('view-essays'))
    else:
        context = {
            'essay_form': EssayForm(),
        }
    return render(request, template, context)

def view_essays(request):
    template = "list_essay.html"
    essays = Essay.objects.all()
    context = {
        'essays': essays,
    }
    return render(request, template, context)

def delete_essay(request, essay_id):
    essay = Essay.objects.get(id=int(essay_id))
    essay.delete()
    return HttpResponseRedirect(reverse_lazy('view-essays'))

def update_essay(request, essay_id):
    template = "update_essay.html"
    essay = Essay.objects.get(id=int(essay_id))
    if request.method == "POST":
        form = EssayForm(request.POST, instance=essay)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('view-essays'))
            context = {
                'essay_form': EssayForm(instance=essay),
            }
    else:
        context = {
            'essay_form': EssayForm(instance=essay),
        }
    return render(request, template, context)


def view_essay(request,essay_id):
	template = "view_essay.html"
	essay = Essay.objects.get(id=int(essay_id))
	context = {
		'essay': essay,
	}
	return render(request, template, context)
"""
def add_enrollment(request):
    template = "add_enrollment.html"
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('view-enrollments'))
    else:
        context = {
            'enrollment_form': EnrollmentForm(),
        }
    return render(request, template, context)

def delete_enrollment(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=int(enrollment_id))
    enrollment.delete()
    return HttpResponseRedirect(reverse_lazy('view-enrollments'))

def update_enrollment(request, enrollment_id):
    template = "update_enrollment.html"
    enrollment = Enrollment.objects.get(id=int(enrollment_id))
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('view-enrollments'))
            context = {
                'enrollment_form': EnrollmentForm(instance=enrollment),
            }
    else:
        context = {
            'enrollment_form': EnrollmentForm(instance=enrollment),
        }
    return render(request, template, context)
"""
def view_enrollments(request):
    template = "list_enrollment.html"
    enrollments = Enrollment.objects.all()
    context = {
        'enrollments': enrollments,
    }
    return render(request, template, context)

def add_word(request):
    template = "add_word.html"

    if request.method == "POST":
        
        form = WordForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        context = {
            'word_form': WordForm(),
        }
    return render(request, template, context)

def add_essay_submission(request,essay_id):
    template = "add_essay_submission.html"
    user_id = request.user.id
    essay = Essay.objects.get(id=essay_id)
    date_today = datetime.datetime.now().replace(tzinfo=utc)
    if request.method == "POST":
        form = EssaySubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('view-essay-submissions'))
    else:
        context = {
            'essay_submission_form': EssaySubmissionForm(initial={'essay':essay.id,'student': user_id,'isChecked':'N','grammar_score':0,'spelling_score':0,'content_score':0,'submitted_date':date_today,'checked_date':date_today}),
            'essay': essay,
        }
    return render(request, template, context)

def view_essay_submissions(request):
    template = "list_essay_submission.html"
    user_id = request.user.id
    #essay_submissions = EssaySubmission.objects.select_related('student','essay').filter(student__id=user_id)
    essays = Essay.objects.select_related('course')
    essay_submissions = EssaySubmission.objects.select_related('student','essay').filter(student__id=user_id)
    courses = Course.objects.all()
    for essay in essays:
        for c in courses:
            present = False
            for s in c.students.all():
                if s.id == user_id:
                    present = True
                    break
            if not present:
                essays = essays.exclude(id=essay.id)
    for essay in essays:
        present = False
        for es in essay_submissions:
            if essay.id == es.essay.id:
                present = True
                break
        if present:
            essays = essays.exclude(id=essay.id)
    date_today = datetime.datetime.now().replace(tzinfo=utc)

    context = {
        'essays': essays,
        'courses': courses,
        'essay_submissions': essay_submissions,
        'date_today': date_today,
    }
    return render(request, template, context)

def delete_essay_submission(request, essay_submission_id):
    essay_submission = EssaySubmission.objects.get(id=int(essay_submission_id))
    essay_submission.delete()
    return HttpResponseRedirect(reverse_lazy('view-essay-submissions'))

def update_essay_submission(request, essay_submission_id):
    template = "update_essay_submission.html"
    essay_submission = EssaySubmission.objects.get(id=int(essay_submission_id))
    if request.method == "POST":
        form = EssaySubmissionForm(request.POST, instance=essay_submission)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('view-essay-submissions'))
            context = {
                'essay_submission_form': EssaySubmissionForm(instance=essay_submission),
            }
    else:
        context = {
            'essay_submission_form': EssaySubmissionForm(instance=essay_submission),
        }
    return render(request, template, context)


def view_essay_submission(request,essay_submission_id):
	template = "view_essay_submission.html"
	essay_submission = EssaySubmission.objects.get(id=int(essay_submission_id))

	spell = SpellChecker()
	# find those words that may be misspelled
	misspelled = spell.unknown(essay_submission.content.split())
	mispelled_list = []
	for word in misspelled:
		current_list = [word,spell.correction(word),spell.candidates(word)]
		mispelled_list.append(current_list)

	complete_text = essay_submission.content
	complete_doc = nlp(complete_text)
	# Remove stop words and punctuation symbols
	words = [token.text for token in complete_doc
	         if not token.is_stop and not token.is_punct]
	word_freq = Counter(words)
	# 5 commonly occurring words with their frequencies
	common_words = word_freq.most_common(5)

	# Unique words
	unique_words = [word for (word, freq) in word_freq.items() if freq == 1]
	context = {
		'essay_submission': essay_submission,
		'mispelled_list': mispelled_list,
		'common_words': common_words,
		'unique_words' : unique_words,
	}
	return render(request, template, context)

def update_profile(request, user_id):
    template = "update_profile.html"
    user = CustomUser.objects.get(id=int(user_id))
    print(user)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('home'))
            context = {
                'update_profile_form': CustomUserChangeForm(instance=user),
            }
    else:
        context = {
            'update_profile_form': CustomUserChangeForm(instance=user),
        }
    return render(request, template, context)

def view_essay_submissions_for_teacher(request):
    user_id = request.user.id
    template = "list_essay_submission_for_teacher.html"
    essay_submissions = EssaySubmission.objects.select_related('essay','student').order_by('isChecked')
    essays = Essay.objects.select_related('course')
    assignments = Assignment.objects.select_related('teacher','course').filter(teacher__id=user_id)
    essays_owned_list = []
    for x in assignments:
        for y in essays:
            if x.course.id == y.course.id:
                essays_owned_list.append(y.id)
    print(essays_owned_list)
    for x in essay_submissions:
        if x.essay.id not in essays_owned_list:
            essay_submissions = essay_submissions.exclude(essay__id=x.essay.id)
    context = {
        'essay_submissions': essay_submissions,
    }
    return render(request, template, context)

def view_essay_submission_for_checking(request, essay_submission_id):
    template = "update_essay_submission.html"
    essay_submission = EssaySubmission.objects.get(id=int(essay_submission_id))
    if request.method == "POST":
        form = EssaySubmissionForm(request.POST, instance=essay_submission)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('view-essay-submissions'))
            context = {
                'essay_submission_form': EssaySubmissionForm(instance=essay_submission),
            }
    else:
        context = {
            'essay_submission_form': EssaySubmissionForm(instance=essay_submission),
        }
    return render(request, template, context)
