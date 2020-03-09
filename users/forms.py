from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime

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
		fields = ('email', 'first_name', 'middle_name', 'last_name', 'id_number')
	def __init__(self, *args, **kwargs):
		super(CustomUserChangeForm, self).__init__(*args, **kwargs)
		self.fields['id_number'].widget = forms.HiddenInput()

class CourseForm(forms.ModelForm):
	start_date = forms.DateField(label='What is the course start date?', widget=forms.SelectDateWidget(years=range(2019,2027)))
	end_date = forms.DateField(label='What is the course end date?', widget=forms.SelectDateWidget(years=range(2019,2027)))
	course_description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))

	class Meta:
		model = Course
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(CourseForm, self).__init__(*args, **kwargs)
		self.fields['students'] = forms.ModelMultipleChoiceField(label="Add Enrolled Students",widget=forms.CheckboxSelectMultiple,queryset=CustomUser.objects.filter(isStudent='S'))
		self.fields['teacher'].widget = forms.HiddenInput()

class EssayForm(forms.ModelForm):
#	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	essay_description = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":50}))
	words = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":50}))
	start_date_time = forms.SplitDateTimeField(label='What is the essay start date and time?', widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'},time_attrs={'type':'time'}))
	end_date_time = forms.SplitDateTimeField(label='What is the essay end date and time?', widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'},time_attrs={'type':'time'}))

	class Meta:
		model = Essay
		fields = '__all__'
	def __init__(self, user_id, *args, **kwargs):
		print(user_id)
		super(EssayForm, self).__init__(*args, **kwargs)
		self.fields['course'].queryset = Course.objects.filter(teacher__id=user_id)

class EssaySubmissionForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	submitted_date = forms.DateTimeField(label='What is the essay submission date?', widget=forms.SelectDateWidget)
	checked_date = forms.DateTimeField(label='What is the essay check date?', widget=forms.SelectDateWidget)
	#student = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))

	class Meta:
		model = EssaySubmission
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(EssaySubmissionForm, self).__init__(*args, **kwargs)
		self.fields['student'].queryset = CustomUser.objects.filter(isStudent='S')
		self.fields['student'].widget = forms.HiddenInput()		
		self.fields['essay'].widget = forms.HiddenInput()	
		self.fields['isChecked'].widget = forms.HiddenInput()
		self.fields['grammar_score'].widget = forms.HiddenInput()
		self.fields['spelling_score'].widget = forms.HiddenInput()
		self.fields['content_score'].widget = forms.HiddenInput()
		#self.fields['submitted_date'].widget = forms.HiddenInput()
		#self.fields['checked_date'].widget = forms.HiddenInput()

class CheckEssaySubmissionForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	submitted_date = forms.DateTimeField(label='What is the essay submission date?', widget=forms.SelectDateWidget)
	checked_date = forms.DateTimeField(label='What is the essay check date?', widget=forms.SelectDateWidget)
	#student = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))

	class Meta:
		model = EssaySubmission
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(CheckEssaySubmissionForm, self).__init__(*args, **kwargs)
		self.fields['student'].queryset = CustomUser.objects.filter(isStudent='S')
		#self.fields['essay'].widget.attrs['disabled'] = True
		self.fields['essay'].widget = forms.HiddenInput()		
		self.fields['student'].widget = forms.HiddenInput()		
		self.fields['content'].widget = forms.HiddenInput()		
		self.fields['isChecked'].widget = forms.HiddenInput()	

class EssaySubmissionCheckingForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))
	submitted_date = forms.DateTimeField(label='What is the essay submission date?', widget=forms.SelectDateWidget)
	checked_date = forms.DateTimeField(label='What is the essay submission date?', widget=forms.SelectDateWidget)
	#student = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":120}))

	class Meta:
		model = EssaySubmission
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(EssaySubmissionForm, self).__init__(*args, **kwargs)
		self.fields['student'].queryset = CustomUser.objects.filter(isStudent='S')