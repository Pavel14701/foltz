from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import Profile, Message
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from user.forms import CustomUserCreationForm, ProfileForm, MessageForm
from common.utils import get_admin_profile_id


def login_user(request: HttpRequest) -> HttpResponseRedirect|HttpResponse:
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not (user := User.objects.get(username=username)):
            messages.error(request, 'Такого пользователя нет в системе')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                request.GET['next'] if 'next' in request.GET else 'account'
            )
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'users/login_register.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')

def register_user(request:HttpRequest) -> HttpResponseRedirect|HttpResponse:
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            action_form_valid(request, form)
        else:
            messages.success(request, 'Во время регистрации возникла ошибка')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def action_form_valid(request:HttpRequest, form:CustomUserCreationForm) -> HttpResponseRedirect:
    user:User = form.save(commit=False)
    user.username = user.username.lower()
    user.save()
    messages.success(request, 'Аккаунт успешно создан!')
    login(request, user)
    return redirect('edit-account')

@login_required
def user_account(request:HttpRequest) -> HttpResponse:
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/account.html', context)

@login_required
def edit_account(request:HttpRequest) -> HttpResponseRedirect|HttpResponse:
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required
def inbox(request:HttpRequest) -> HttpResponse:
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {
        'messageRequests': messageRequests, 
        'unreadCount': unreadCount
    }
    return render(request, 'users/inbox.html', context)


@login_required
def view_message(request:HttpRequest, pk:int|str) -> HttpResponse:
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def create_message(request:HttpRequest) -> HttpResponseRedirect|HttpResponse:
    recipient = get_admin_profile_id()
    form = MessageForm()
    if not (sender := request.user.profile):
        messages.success(request, 'При отправке сообщения произошла ошибка!')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            return message_form_valid(form, sender, recipient, request)    
    context = {'recipient': recipient, 'form': form}
    return render(request, 
        'users/message_form.html', context)

def message_form_valid(form:MessageForm, sender:any, recipient:Profile, request:HttpRequest) -> HttpResponseRedirect:
    message:Message = form.save(commit=False)
    message.sender = sender
    message.recipient = recipient
    if sender:
        message.name = sender.name
        message.email = sender.email
    message.save()
    messages.success(request, 'Сообщение успешно отправлено!')
    return redirect('user-profile', username=recipient.username)