from django.urls import path
from .views import *

urlpatterns = [
    path('users/add', addUser, name="addUser"),
    path('chats/add', addChat, name="addChat"),
    path('messages/add', addMessage, name="addMessage"),
    path('chats/get', getChats, name="getChats"),
    path('messages/get', getMessages, name="getMessages"),
]
