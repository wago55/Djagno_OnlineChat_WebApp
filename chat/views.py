from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateChatRoomForm, SendChatForm
from .models import Chat, ChatRoom
from django.urls import reverse_lazy
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse
from . import forms



class ChatEnterRoomView(ListView):
    template_name = "chat/chat_enter.html"
    model = ChatRoom


class CreateChatRoomView(CreateView):
    template_name = "chat/chat_room_create.html"
    model = ChatRoom
    form_class = CreateChatRoomForm
    success_url = reverse_lazy("chat:chat_enter")
    
    def form_valid(self, form):
        chat_room = form.save(commit=False)
        user_id = self.request.user.id
        chat_room.username_id = user_id
        chat_room.save()
        return super().form_valid(form)


class ChatRoomUpdate(UpdateView):
    template_name = "chat/chat_room_update.html"
    model = ChatRoom
    form_class = CreateChatRoomForm
    success_url = reverse_lazy("chat:chat_enter")


class ChatroomDelete(DeleteView):
    template_name = "chat/chat_room_delete.html"
    model = ChatRoom
    success_url = reverse_lazy("chat:chat_enter")


def send_chat(request, chatroom_id):
    saved_chat = cache.get(f'saved_chat-chatroom_id={chatroom_id}-user_id={request.user.id}', '')
    send_chat_form = forms.SendChatForm(request.POST or None, initial={'chat': saved_chat})
    chat_room = get_object_or_404(ChatRoom, id=chatroom_id)
    chat = Chat.objects.fetch_by_chat_id(chatroom_id)

    if send_chat_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        send_chat_form.instance.chatroom = chat_room
        send_chat_form.instance.user = request.user
        send_chat_form.save()
        cache.delete(f'saved_chat-chatroom_id={chatroom_id}-user_id={request.user.id}')
        return redirect('chat:send_chat', chatroom_id=chatroom_id)

    return render(request, 'chat/send_chat.html',  context={
        'send_chat_form': send_chat_form,
        'chat_room': chat_room,
        'chat': chat,
    })


def save_chat(request):
    if request.is_ajax:
        chat = request.GET.get('chat')
        chatroom_id = request.GET.get('chatroom_id')
        print(chat)
        print(chatroom_id)
        if chat and chatroom_id:
            cache.set(f'saved_chat-chatroom_id={chatroom_id}-user_id={request.user.id}', chat)
            return JsonResponse({'message': '一時保存しました'})









