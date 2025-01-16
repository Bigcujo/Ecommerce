from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError

#forms will go down here


# this is the user registar form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  # Do not include 'confirm_password' here

    def __init__(self, *args, **kwargs):
                super(UserRegistrationForm, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_method = 'post'
                self.helper.layout = Layout(
                    Row(
                        Column('username', css_class='form-group col-md-6 mb-0'),
                        Column('email', css_class='form-group col-md-6 mb-0'),
                        css_class='row'
                    ),
                    'password',
                    'confirm_password',
                    Submit('submit', 'Sign up ', css_class='btn btn-outline-info')
                )    
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user