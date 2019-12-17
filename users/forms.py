from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import *

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
    ))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'id_number','isStudent')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'id_number','isStudent')

class CourseForm(forms.ModelForm):
	end_date = forms.DateField(label='What is the course end date?', widget=forms.SelectDateWidget)
	class Meta:
		model = Course
		fields = '__all__'

class EssayForm(forms.ModelForm):
#	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	start_date_time = forms.DateTimeField(label='What is the essay start date?', widget=forms.SelectDateWidget)
	end_date_time = forms.DateTimeField(label='What is the essay end date?', widget=forms.SelectDateWidget)

	class Meta:
		model = Essay
		fields = '__all__'

class EssaySubmissionForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	class Meta:
		model = EssaySubmission
		fields = '__all__'

class EnrollmentForm(forms.ModelForm):
	class Meta:
		model = Enrollment
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(EnrollmentForm, self).__init__(*args, **kwargs)
		self.fields['student'].queryset = CustomUser.objects.filter(isStudent='S')

class WordForm(forms.ModelForm):

	class Meta:
		model = Word
		fields = '__all__'