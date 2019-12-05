from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from spellchecker import SpellChecker
from collections import Counter
import spacy
nlp = spacy.load('en_core_web_sm')

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def add_course(request):
    template = "add_course.html"

    if request.method == "POST":
        
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        context = {
            'course_form': CourseForm(),
        }
    return render(request, template, context)

def add_essay(request):
    template = "add_essay.html"

    if request.method == "POST":
        
        form = EssayForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        context = {
            'essay_form': EssayForm(),
        }
    return render(request, template, context)

def view_essay(request,essay_id):
	template = "view_essay.html"
	essay = Essay.objects.get(id=int(essay_id))
	spell = SpellChecker()
	# find those words that may be misspelled
	misspelled = spell.unknown(essay.content.split())
	mispelled_list = []
	for word in misspelled:
		current_list = [word,spell.correction(word),spell.candidates(word)]
		mispelled_list.append(current_list)

	complete_text = essay.content
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
		'essay': essay,
		'mispelled_list': mispelled_list,
		'common_words': common_words,
		'unique_words' : unique_words,
	}
	return render(request, template, context)