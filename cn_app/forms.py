from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Comment, SignUp


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length = 30, required = True)
    email = forms.EmailField(max_length = 100, required = True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')


class EmailSignUpForm(forms.ModelForm):
    email = forms.EmailField(widget = forms.TextInput(attrs = {
            'type':'email',
            'name':'email',
            'placeholder':"Type in your email"
    }), label = '')

    class Meta:
        model = SignUp
        fields = ('email',)
