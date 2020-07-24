from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserUpdateForm
from authapp.models import ShopUser


def login(request):
    redirect = request.GET.get('redirect', '')
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'redirect' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['redirect'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'title': 'Вход',
        'form': form,
        'redirect': redirect,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.send_verify_mail():
                message = 'Сообщение для подтверждения аккаунта отправлено'
                print(message)
            else:
                message = 'Ошибка отправки сообщения'
                print(message)
            return HttpResponseRedirect(reverse('auth:send_confirm', kwargs={'message': message}))
            # return HttpResponseRedirect(reverse('main:index', kwargs={'message': message}))
    else:
        form = ShopUserRegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


def update(request):
    if request.method == 'POST':
        form = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)

    context = {
        'title': 'Редактирование профиля',
        'form': form,
    }
    return render(request, 'authapp/update.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        print(user)
        print(user.activation_key)
        print(user.is_activation_key_expired())
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))
