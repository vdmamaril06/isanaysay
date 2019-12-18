from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'middle_name', 'last_name', 'id_number','isStudent']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Essay)
admin.site.register(EssaySubmission)
admin.site.register(Word)
admin.site.register(Criterion)
admin.site.register(Enrollment)
admin.site.register(Score)
