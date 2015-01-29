__author__ = 'sirine'
from blog.models import Condidate,Votant
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class VotantForm(forms.ModelForm):
    class Meta:
        model = Votant
        fields = ('first_name', 'last_name', 'age', 'num_cin', 'nationality', 'sex', 'adress')

class CondidateForm(forms.ModelForm):
    class Meta:
        model = Condidate
        fields = ('first_name', 'last_name', 'age', 'num_cin', 'nationality', 'job', 'sex', 'adress', 'picture', 'evenement', 'contenu')
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control input-lg', 'placeholder': 'contenu'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField()
    topic = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(label="votre adresse mail")


