# File Name		: views.py
# Version	    : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: ユーザ登録・ログインに関する各ページの設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.08 ログインの有無によるメッセージ変更の追加
#                             ユーザ登録の失敗・成功ページを追加


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import RegistUserForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Users


class HomeView(ListView):
    template_name = 'accounts/home.html'
    model = Users

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            id=self.request.user.id
        )

        return query


class RegistUserView(CreateView):
    template_name = 'accounts/regist_user.html'
    form_class = RegistUserForm


class RegistUserSuccessView(TemplateView):
    template_name = "accounts/regist_user_success.html"


class RegistUserFailedView(TemplateView):
    template_name = "accounts/regist_user_failed.html"


class UserLoginView(FormView):
    template_name = "accounts/user_login.html"
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('accounts:login_success')
        return redirect('accounts:login_failed')


class UserLoginSuccessView(TemplateView):
    template_name = "accounts/user_login_success.html"


class UserLoginFailedView(TemplateView):
    template_name = "accounts/user_login_failed.html"
    

class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:user_login')