from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
