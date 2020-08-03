import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json

from mainapp.models import ProductCategory, Product


def index(request):
    context = {
        'page_title': 'Interior',
    }
    return render(request, 'mainapp/index.html', context)


def products(request, page=1):
    categories = ProductCategory.objects.all()
    # products_list = Product.objects.all()
    hot_product_pk = random.choice(Product.objects.filter(is_active=True).values_list('pk', flat=True))
    hot_product = Product.objects.get(pk=hot_product_pk)
    same_products = hot_product.category.product_set.filter(is_active=True).exclude(pk=hot_product.pk)

    products_paginator = Paginator(same_products, 1)
    try:
        same_products = products_paginator.page(page)
    except PageNotAnInteger:
        same_products = products_paginator.page(1)
    except EmptyPage:
        same_products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Products',
        'categories': categories,
        # 'products': products_list[:3],
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/product-details.html', context)


def category_products(request, pk, page=1):
    categories = ProductCategory.objects.all()

    if pk == '0':
        category = {'pk': 0, 'name': 'Все'}
        products_list_category = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products_list_category = category.product_set.filter(is_active=True)

    products_paginator = Paginator(products_list_category, 3)
    try:
        products_list_category = products_paginator.page(page)
    except PageNotAnInteger:
        products_list_category = products_paginator.page(1)
    except EmptyPage:
        products_list_category = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Products',
        'categories': categories,
        'products': products_list_category,
        'category': category,
    }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    categories = ProductCategory.objects.all()
    product = get_object_or_404(Product, pk=pk)
    context = {
        'page_title': 'каталог',
        'categories': categories,
        'category': product.category,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    with open('locations.json', 'r', encoding="utf-8") as file:
        locations = json.load(file)

    context = {
        'page_title': 'Contacts',
        'locations': locations,
    }

    return render(request, 'mainapp/contacts.html', context)


def product_detail_async(request, pk):
    if request.is_ajax():
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({
                'product_price': product.price,
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })
