from datetime import timedelta, datetime
from pytz import timezone
from django.core.mail import send_mail
from django.db import models

from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.utils.timezone import now

from geekshop import settings


def get_activation_key_expires():
    return datetime.now().astimezone(timezone(settings.TIME_ZONE)) + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField('Возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    id_for_friends = models.CharField('Код для пригашения друзей', max_length=8, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_expires)
    # activation_key_expires = models.DateTimeField(auto_now_add=True)

    def is_activation_key_expired(self):
        # return datetime.now() > (self.activation_key_expires + timedelta(hours=48))
        return datetime.now().astimezone(timezone(settings.TIME_ZONE)) > self.activation_key_expires

    def send_verify_mail(self):
        verify_link = reverse(
            'auth:verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key,
            },
        )
        title = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE,
                                primary_key=True)
    tagline = models.CharField(verbose_name='теги', max_length=128,
                               blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512,
                               blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, default=MALE)
