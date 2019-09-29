from django import forms
from .models import *
from django.contrib.auth.models import User


class PostCreateViewForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'question_image', 'question_file']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'created', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }



class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password did not match")

            return confirm_password


# contact form
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True)
