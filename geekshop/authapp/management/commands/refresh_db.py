from django.core.management.base import BaseCommand

from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    help = 'Fill DB.shopuserprofile new data from shopuser'

    def handle(self, *args, **options):
        users_to_update = ShopUser.objects.filter(shopuserprofile__isnull=True)
        print(users_to_update.count())
        for user in users_to_update:
            ShopUserProfile.objects.create(user=user)
