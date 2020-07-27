from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserUpdateForm, ShopUserProfileUpdateForm
from authapp.models import ShopUser, ShopUserProfile


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
        profile_form = ShopUserProfileUpdateForm(request.POST, request.FILES, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            # profile_form.save() # - не нужно пока есть сигнал
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)
        profile_form = ShopUserProfileUpdateForm(instance=request.user.shopuserprofile)

    context = {
        'title': 'Редактирование профиля',
        'form': form,
        'profile_form': profile_form,
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
            user.activation_key = ''
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)
    else:
        instance.shopuserprofile.save()
