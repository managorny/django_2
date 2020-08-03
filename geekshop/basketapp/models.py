from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_datetime = models.DateTimeField('дата добавления', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        # _items = self.user.basket_set.all()
        # return sum(self.user.basket.values_list('quantity', flat=True))
        return sum(map(lambda x: x.quantity, self.user.basket.all()))

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        # _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return sum(map(lambda x: x.product_cost, self.user.basket.all()))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
