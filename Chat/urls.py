from django.urls import path
from . import views

urlpatterns = [

    path('', views.all_chats, name='chats'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('all_chats/', views.all_chats, name='all_chats'),
    path('my_chats/', views.my_chats, name='my_chats'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('edit_chat/<int:chat_id>/', views.edit_chat, name='edit_chat'),
    path('delete_chat/<int:chat_id>', views.delete_chat, name='delete_chat'),
    path('logout/', views.user_logout, name='logout'),
    path('chat/<int:chat_id>/like/', views.like_chat, name='like_chat'),
]
