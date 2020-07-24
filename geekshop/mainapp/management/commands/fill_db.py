import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    with open(os.path.join(settings.JSON_PATH, f'{file_name}.json'), encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    help = 'Fill empty DB new data, if DB not empty, delete old data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        Product.objects.all().delete()  # т.к. у меня нельзя удалить категорию каскадом
        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category['fields']) for category in categories]

        products = load_from_json('products')

        #     # явно сделал так, что видно, что id съезжают, если несколько раз запускать с ошибками,
        #     # рабочий код у категорий каждый раз делает инкремент id. Пришлось поправить json.
        #     # TODO сделать обработку dumpdata json лучше, чтобы не создавать json руками и не было лишних циклов.
        # for product in products:
        #     product_fields = product['fields']
        #     category_id = product_fields['category']
        #     _category = ProductCategory.objects.filter(pk=category_id).first()
        #     [Product.objects.create(**product['fields']) for product in products]

        for product in products:
            product_fields = product['fields']
            category_name = product_fields['category']
            _category = ProductCategory.objects.filter(name=category_name).first()
            product_fields['category'] = _category
            Product.objects.create(**product_fields)

        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='admin@geekshop.local', password='geekbrains')
