from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile


class StaffSignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="A valid email address.")
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['history_of_illness','name','gender']

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','gender']




