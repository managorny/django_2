from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from geekshop.settings import LOGIN_URL


@login_required
def index(request, page=1):

    basket = request.user.basket.select_related().all()

    products_paginator = Paginator(basket, 2)
    try:
        basket = products_paginator.page(page)
    except PageNotAnInteger:
        basket = products_paginator.page(1)
    except EmptyPage:
        basket = products_paginator.page(products_paginator.num_pages)

    context = {
        'basket': basket
    }
    return render(request, 'basketapp/index.html', context)


@login_required(redirect_field_name='redirect')
def add_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = request.user.basket.filter(product=pk).first()
    # basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:index'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_product(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(reverse('basket:index'))


@login_required
def change(request, pk, quantity):
    if request.is_ajax():
        basket = get_object_or_404(Basket, pk=pk)
        if int(quantity) <= 0:
            basket.delete()
        else:
            basket.quantity = int(quantity)
            basket.save()

        context = {
            'basket': request.user.basket.all(),
        }
        result = render_to_string('basketapp/includes/inc__basket_list.html', context, request=request)

        return JsonResponse({'result': result})
        # return JsonResponse({
        #     'total_cost': basket.total_cost,
        #     'total_quantity': basket.total_quantity,
        #     'product_cost': basket.product_cost,
        # })


# @receiver(pre_save, sender=OrderItem) - see ordersapp
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


# @receiver(pre_delete, sender=OrderItem) - see ordersapp
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    if instance.product.quantity >= instance.quantity:
        instance.product.quantity += instance.quantity
    instance.product.save()
