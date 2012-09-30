from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddBooksForm(forms.Form):
    bookname = forms.CharField()
    authorname = forms.CharField()

