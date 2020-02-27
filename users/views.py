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
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from spacy.lang.en.stop_words import STOP_WORDS 
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
import grammar_check
import re

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
    user_id = request.user.id
    form = EssayForm(user_id)
    if request.method == "POST":
        form = EssayForm(user_id,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('view-essays'))
    else:
        context = {
            'essay_form': form,
        }
    return render(request, template, context)

def view_essays(request):
    template = "list_essay.html"
    user_id = request.user.id
    essays = Essay.objects.filter(course__teacher__id=user_id)
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
    user_id = request.user.id
    essay = Essay.objects.get(id=int(essay_id))
    if request.method == "POST":
        form = EssayForm(user_id,request.POST, instance=essay)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy('view-essays'))
            context = {
                'essay_form': EssayForm(user_id,instance=essay),
            }
    else:
        context = {
            'essay_form': EssayForm(user_id,instance=essay),
        }
    return render(request, template, context)


def view_essay(request,essay_id):
	template = "view_essay.html"
	essay = Essay.objects.get(id=int(essay_id))
	context = {
		'essay': essay,
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
            print("This is the content score: " + str(form.cleaned_data['content_score']))
            instance = form.save(commit=False)
            instance.content_score = grade_for_essay_content(essay.words,form['content'].value())['counter']
            instance.spelling_score = grade_for_spelling(form['content'].value())['score']
            instance.grammar_score = grade_for_grammar(form['content'].value())["score"]
            print("This is the content score 2: " + str(instance.content_score))
            instance.save()
            return HttpResponseRedirect(reverse_lazy('view-essay-submissions'))
    else:
        context = {
            'essay_submission_form': EssaySubmissionForm(initial={'essay':essay.id,'student': user_id,'isChecked':'N','grammar_score':0,'spelling_score':0,'submitted_date':date_today,'checked_date':date_today}),
            'essay': essay,
        }
    return render(request, template, context)

def view_essay_submissions(request):
    template = "list_essay_submission.html"
    user_id = request.user.id
    print(user_id)
    #essay_submissions = EssaySubmission.objects.select_related('student','essay').filter(student__id=user_id)
    essays = Essay.objects.select_related('course')
    essay_submissions = EssaySubmission.objects.select_related('student','essay').filter(student__id=user_id)
    courses = Course.objects.all()
    for essay in essays:
        present = False
        for s in essay.course.students.all():
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
    courses = Course.objects.select_related('teacher').filter(teacher__id=user_id)
    essays_owned_list = []
    for x in courses:
        for y in essays:
            if x.id == y.course.id:
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
    user_id = request.user.id
    date_today = datetime.datetime.now().replace(tzinfo=utc)
    template = "check_essay_submission.html"
    essay_submission = EssaySubmission.objects.get(id=int(essay_submission_id))
    essay_content_result = grade_for_essay_content(essay_submission.essay.words,essay_submission.content)
    spelling_result = grade_for_spelling(essay_submission.content)
    grammar_result = grade_for_grammar(essay_submission.content)
    #print(essay_submission_essay)
    if request.method == "POST":
        form = CheckEssaySubmissionForm(request.POST, instance=essay_submission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('view-essay-submissions-for-teacher'))
            """
            context = {
                'essay_submission_form': CheckEssaySubmissionForm(instance=essay_submission,initial={'essay':essay_submission.essay.id,'student': essay_submission.student,'isChecked':'Y','submitted_date':essay_submission.submitted_date,'checked_date':date_today}),
                'essay_submission' : essay_submission,
            }"""
    else:
        context = {
            'essay_submission_form': CheckEssaySubmissionForm(instance=essay_submission,initial={'essay':essay_submission.essay.id,'student': essay_submission.student,'isChecked':'Y','submitted_date':essay_submission.submitted_date,'checked_date':date_today}),
            'essay_submission' : essay_submission,
            'unmatched_words': essay_content_result["unmatched_words"],
            'matched_words': essay_content_result["matched_words"],
            'mispelled_words': spelling_result["mispelled_words"],
            'lexically_ambiguous_sentences': grammar_result["lexically_ambiguous_sentences"],
            'gramatically_ambiguous_sentences': grammar_result["gramatically_ambiguous_sentences"],
            'essay_content_individual_score': essay_content_result["individual_score"],
            'spelling_individual_score': spelling_result["individual_score"],
            'grammar_individual_score': grammar_result["individual_score"],
        }
    return render(request, template, context)

def grade_for_essay_content(words,essay):
    words = words.split(',')
    result = {'counter':0,'matched_words':[],'unmatched_words':[],'individual_socre':0}
    for word in words:
        word_found = False
        for essay_word in essay.split():
            print(essay_word)
            if word.lower() == essay_word.lower():
                result["counter"] += 1
                word_found = True
                break
            else:
                token = nlp(essay_word)[0]
                for syn in token._.wordnet.synsets():
                    if word_found:
                        break
                    for l in syn.lemmas():
                        print(l.name().lower())
                        if word.lower() == l.name().lower():
                            result["counter"] += 1
                            word_found = True
                            break
        if not word_found:
            result["unmatched_words"].append(word)
        else: 
            result["matched_words"].append(word)
    result["counter"] = (result["counter"]/len(words))*100
    result["individual_score"] = 1 / len(words) * 100
    return result

def tokens(sent):
        nlpe = spacy.load('en_core_web_sm')
        print(nlpe(sent))
        return nlpe(sent)

def grade_for_spelling(line):
    result = {'score':0,'mispelled_words':[],'individual_socre':0}
    line = removePunct(line.lower())
    number_of_mispelled_words = 0
    total = 0
    print("TOKEN = " + str(tokens(line)))
    for i in tokens(line):
        strip = i.text.rstrip()
        if strip != "":
            token = nlp(strip)[0]
            if not token._.wordnet.synsets():
                lexeme = nlp.vocab[strip]
                if lexeme.is_stop == True:    # <--- Check whether it's in stopword list
                    total += 1
                    continue
                else:
                    total += 1
                    result["mispelled_words"].append(strip)
                    number_of_mispelled_words += 1
            else: 
                total += 1
                continue
    result["score"] = (total - number_of_mispelled_words) / total * 100
    result["individual_score"] = 1 / total * 100
    return result 


def removePunct(str):
        return  "".join(c for c in str if c not in ('!','.',':',',','-','&','#','%','$'))

def grade_for_grammar(essay):
    result = {'score':0,'lexically_ambiguous_sentences':[],'gramatically_ambiguous_sentences':[],'individual_socre':0}
    regex_sentences = essay.split('.')
    regex_sentences = [string for string in regex_sentences if string != ""]
    sentences = []
    for x in regex_sentences:
        r = re.findall(r"[^\s]",x)
        if r:
            sentences.append(x.replace("\r","").replace("\n","").replace("\t",""))
    print("The sentences are the following: " + str(sentences))
    tool = grammar_check.LanguageTool('en-US')
    incorrect = 0
    for sentence in sentences:
        matches = tool.check(sentence)
        words = sentence.split()
        lexical_ambiguous_words_count = 0
        if len(matches) > 0:
            incorrect += 1
            result["gramatically_ambiguous_sentences"].append(sentence)
            continue
        for word in words:
            if word != "":
                token = nlp(word)[0]
                if token._.wordnet.synsets():
                    lexeme = nlp.vocab[word]
                    if lexeme.is_stop != True:    # <--- Check whether it's in stopword list
                        if len(token._.wordnet.synsets()) >= 5:
                            print(str(word) + " has " + str(len(token._.wordnet.synsets())) + " meanings.")
                            lexical_ambiguous_words_count += 1
        if (lexical_ambiguous_words_count / len(words)) > 0.1:
            incorrect += 1
            result["lexically_ambiguous_sentences"].append(sentence)
            continue
    result["score"] = (len(sentences) - incorrect) / len(sentences) * 100
    result["individual_score"] = 1 / len(sentences) * 100
    return result 

