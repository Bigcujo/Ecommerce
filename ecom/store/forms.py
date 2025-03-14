from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from .models import CustomUser, Profile
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
    


# user update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)


    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

# update user password
class ChangePasswordForm(SetPasswordForm):
     class Meta:
          model = CustomUser
          fields = ['new_password1', 'new_password2']

#update user info
class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )

