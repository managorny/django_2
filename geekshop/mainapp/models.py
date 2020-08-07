from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('Название', max_length=128, unique=True)
    description = models.TextField('Описание', max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')
    name = models.CharField('Название', max_length=128)
    short_description = models.CharField('Краткое описание', max_length=128, blank=True)
    description = models.TextField('Описание', blank=True)
    quantity = models.PositiveIntegerField('Количество', default=0)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=0, default=0)
    image = models.ImageField(upload_to='products_images', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    @staticmethod
    def get_active_items():
        return Product.objects.select_related().filter(category__is_active=True, is_active=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
