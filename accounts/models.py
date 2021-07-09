# File Name		: models.py
# Version	    : V1.1
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose       : 

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.08 ユーザ登録の成功ページを追加




from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        if not email:
            raise ValueError('Enter Email')

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BigIntegerField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'Users'

    def get_absolute_url(self):
        return reverse_lazy('accounts:regist_success')