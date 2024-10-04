from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Profile, Rechat
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.files.storage import default_storage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('login') 
    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('all_chats')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')    


def all_chats(request):
    chats = Chat.objects.all().order_by('-created_at')
    context = {
        'chats': chats,
        'user': request.user,
        'active_section': 'all_chats',
    }
    return render(request, 'Chat/all_chats.html', context)

def my_chats(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'chats': chats,
        'user': request.user,
        'active_section': 'my_chats',
    }
    return render(request, 'Chat/all_chats.html', context)


@login_required
def create_chat(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        attachments = request.FILES.get('attachments')

        if not text:
            return render(request, 'create_tweet.html', {'error': 'Tweet text is required'})
        
        chat = Chat(user=request.user, text=text, attachments=attachments)
        chat.save()
        return redirect('all_chats')
    
    return render(request, 'Chat/create_chat.html')


@login_required
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if chat.user != request.user:
        return redirect('all_chats')

    if request.method == 'POST':
        text = request.POST.get('text')
        remove_attachment = 'remove_attachment' in request.POST

        chat.text = text

        if not text:
            return render(request, 'edit_chat.html', {'chat': chat, 'error': 'Chat text is required'})

        if remove_attachment:
            if chat.attachments:
                default_storage.delete(chat.attachments.name)
            chat.attachments = None
        elif 'attachments' in request.FILES:
            chat.attachments = request.FILES['attachments']
                    
        chat.save()

        return redirect('all_chats') 

    return render(request, 'Chat/edit_chat.html', {'chat': chat})


@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    
    if chat.user != request.user:
        return redirect('all_chats')
    
    if request.method == 'POST':        
        chat.delete()
        return redirect('all_chats')

    return render(request, 'Chat/delete_chat.html', {'chat': chat})

@login_required
def like_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user in chat.likes.all():
        chat.likes.remove(request.user)
    else:
        chat.likes.add(request.user)
    return redirect('all_chats')
