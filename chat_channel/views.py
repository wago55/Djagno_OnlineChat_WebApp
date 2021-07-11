# File Name		: views.py
# Version	    : V2.2
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: チャット機能に関する各ページの設定

# Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.12 チャットルーム認証機能に対応
# V2.0 : 松岡修平, 2021.06.15 参加者と部屋情報の関係を登録
# V2.1 : 高橋龍平, 2021.06.18 カウントダウン機能に対応
# V2.2 : 平澤巧望, 2021.07.10 非ログイン時のエラー処理の追加

from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from .forms import CreateChatRoomForm, LoginChatRoomForm
from django.contrib.auth import authenticate, login, logout
from .models import ChatRoomChannel, JoinChatRoom
from django.urls import reverse_lazy
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
import json
import random

import chat_channel

#def chat(request):

#    return render(request, 'chat_channel/chat.html')

class TimerView(TemplateView):
    template_name = "chat_channel/timer.html"

class Chat(TemplateView):
    template_name = "chat_channel/chat.html"
    model = ChatRoomChannel

"""
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['room_list'] = ChatRoomChannel.objects.all()
            return context
                
        def rooms(request):
            rooms_f = ChatRoomChannel.objects.all() 
            rooms_f_html = []
            for instance in ChatRoomChannel.objects.all():  # it's not serialization, but extracting of the useful fields
                rooms_f_html.append({'pk': instance.pk, 'room_name': instance.room_name, 'chatroom_id': instance.chatroom_id, 'password': instance.password})
            rooms_dic = {'rooms_f': rooms_f, 'ac_tab_n': 'ac_tab', 'rooms_f_html': rooms_f_html}
            return render(request, 'chat_channel/chat.html', rooms_dic)
    """


class LoginChatRoomView(LoginRequiredMixin, FormView):
    template_name = "chat_channel/chat_room_login.html"
    form_class = LoginChatRoomForm

    def post(self, request, *args, **kwargs):
        chatroom_id = request.POST['chatroom_id']
        password = request.POST['password']
        # self.request.user_name 

        chat_room = ChatRoomChannel.objects.filter(chatroom_id=chatroom_id)
        if chat_room.first() is not None:
            chat_room = ChatRoomChannel.objects.get(chatroom_id=chatroom_id)
            if chat_room.password == password:
#                return HttpResponse("Success.") # テスト用
                params = {
                    'room_name' : chat_room.room_name,
                    'user_name' : self.request.user.username,
                    'chatroom_id' : chat_room.chatroom_id, #idでフィルターをかけるために追加
                }
                #入室成功時JoinChatRoomにデータを追加
                obj = JoinChatRoom()
                obj.room_id = chatroom_id
                #strGroupNameと一致させるために修正
                obj.room_name = 'chat_' + chat_room.room_name
                obj.username = self.request.user.username
                obj.save()
                return render(request, 'chat_channel/chat.html', params)
            return redirect('chat_channel:login_failed')
        return redirect('chat_channel:login_failed')
    

class LoginChatRoomFailedView(TemplateView):
    template_name = "chat_channel/chat_room_login_failed.html"


class CreateChatRoomView(LoginRequiredMixin, CreateView):
    template_name = "chat_channel/chat_room_create.html"
    model = ChatRoomChannel
    form_class = CreateChatRoomForm
    success_url = reverse_lazy("chat_channel:chat_room_login")

    def form_valid(self, form):
        chat_room = form.save(commit=False)
        user_id = self.request.user.id
        chat_room.username_id = user_id
        chat_room.save()
        return super().form_valid(form)
#        return render(self.request, 'chat_channel/chat_room_create_success.html', {'form' : form})

class CreateChatRoomSuccessView(TemplateView):
    template_name = "chat_channel/chat_room_create_success.html"


class CreateChatRoomFailedView(TemplateView):
    template_name = "chat_channel/chat_room_create_failed.html"

class ChatRoomLeaveView(TemplateView):
    template_name = "chat_channel/chat_room_leave.html"


def room_detail(request, room_id):
    num = room_id
    data = JoinChatRoom.objects.filter(room_id=num)
    #sikai = random.choice(data)
    params = {
        #'sikai' : sikai,
        'data' : data,
    }
    return render(request, 'chat_channel/chat_room_detail.html', params)

def delete_joinchatroom(request, num):
    obj = JoinChatRoom.objects.get(id=num)
    if(request.method == 'POST'):
        num_id = obj.room_id
        obj.delete()
        return redirect('chat_channel:chat_room_detail',room_id=num_id)
    params = {
        'data': obj,
    }
    return render(request, 'chat_channel/delete_joinchatroom.html', params)