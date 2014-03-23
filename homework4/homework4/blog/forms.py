from django import forms
from django.contrib.auth.models import User
from models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', )
        widgets = {
            'title': forms.TextInput(attrs={'id': 'blog-title'}),
            'content': forms.Textarea(attrs={'id': 'blog-content'}),
            'image': forms.FileInput(attrs={'id:': 'blog-image'})
        }

class RegistrationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'   
    username = forms.CharField(max_length = 20,
                                label='User Name',
                                widget = forms.TextInput(attrs={'id': 'usname'}))
    first_name = forms.CharField(max_length = 20,
                                label='First Name',
                                widget = forms.TextInput(attrs={'id': 'fsname'}))
    last_name = forms.CharField(max_length = 20,
                                label='Last Name',
                                widget = forms.TextInput(attrs={'id': 'lsname'}))
    email = forms.EmailField(max_length = 40,
                                label='Email',
                                widget = forms.EmailInput(attrs={'id': 'email'}))
    password1 = forms.CharField(max_length = 200,
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'id': 'ps1'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'id': 'ps2'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username
