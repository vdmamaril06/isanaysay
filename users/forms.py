from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'id_number','isStudent')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'id_number','isStudent')

class CourseForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = '__all__'

class EssayForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	class Meta:
		model = Essay
		fields = '__all__'

class WordForm(forms.ModelForm):

	class Meta:
		model = Word
		fields = '__all__'