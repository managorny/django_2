from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    PREPARING = 'P'
    SENT_FOR_ASSEMBLY = 'S'
    ASSEMBLY = 'A'
    PAID = 'D'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (PREPARING, 'формируется'),
        (SENT_FOR_ASSEMBLY, 'отправлен на сборку'),
        (ASSEMBLY, 'собирается'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=PREPARING)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    @property
    def total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, items)))

    @property
    def product_type_quantity(self):
        items = self.orderitems.all()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def get_summary(self):
        items = self.orderitems.select_related().all()
        return {
            "total_quantity": sum(list(map(lambda x: x.quantity, items))),
            "type_quantity": len(items),
            "total_cost": sum(list(map(lambda x: x.quantity * x.product.price, items))),
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
