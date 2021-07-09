# File Name		: urls.py
# Version	    : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: 

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.08 ログインの有無によるメッセージ変更の追加
#                             ユーザ登録の失敗・成功ページを追加


from django.urls import path, include
from .views import HomeView, RegistUserSuccessView, RegistUserView, UserLoginView, UserLogoutView
from .views import RegistUserSuccessView, RegistUserFailedView, UserLoginSuccessView, UserLoginFailedView

app_name = "accounts"

urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('regist_user/', RegistUserView.as_view(), name="regist_user"),
    path('regist_user_success/', RegistUserSuccessView.as_view(), name="regist_success"),
    path('regist_user_failed/', RegistUserFailedView.as_view(), name="regist_failed"),
    path('user_login/', UserLoginView.as_view(), name="user_login"),
    path('user_login_success/', UserLoginSuccessView.as_view(), name="login_success"),
    path('user_login_failed/', UserLoginFailedView.as_view(), name="login_failed"),
    path('user_logout/', UserLogoutView.as_view(), name="user_logout"),
]
