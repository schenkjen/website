from django import forms
from messages.forms import ComposeForm

class MultiComposeForm(ComposeForm):
	subject = forms.CharField(widget=forms.TextInput(attrs={'class':'width100'}))
	body = forms.CharField(widget=forms.Textarea(attrs={'class':'width100'}))
	search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'small-input'}))
