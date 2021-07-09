# File Name		: forms.py
# Version	    : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose       : 

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 和合雅輝, 2021.06.29 revise validation error


from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password


class RegistUserForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メール')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        paslen = []
        paslen = password
        if len(paslen) < 8:
            raise forms.ValidationError("パスワードが短過ぎます。最低8文字以上必要です。")
        elif password == username:
            raise forms.ValidationError("パスワードをユーザー名と同じにすることはできません。")

        return password

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
