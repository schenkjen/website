''' jaxerorg forms.py '''
from django import forms
from django.contrib.auth.models import User
from sjphoto.base.models import Photo
class LoginForm(forms.Form):
    username = forms.CharField(widget=(forms.TextInput(attrs={'style':'height=25px'})))
    password = forms.CharField(widget=(forms.PasswordInput(attrs={'style':'height=25px'})))
    next = forms.CharField(required=False, widget=(forms.HiddenInput()))

class PhotoUploader(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image', ]
