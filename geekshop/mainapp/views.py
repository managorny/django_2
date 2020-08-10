import random

from django.core.cache import cache
from django.views.decorators.cache import cache_page, never_cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json

from mainapp.models import ProductCategory, Product

from geekshop.settings import LOW_CACHE


def get_category_list():
    if LOW_CACHE:
        key = 'category_list'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if LOW_CACHE:
        key = f'productcategory_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_in_productcategory(pk):
    if LOW_CACHE:
        key = f'products_in_productcategory_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True,category__is_active=True)


def index(request):
    context = {
        'page_title': 'Interior',
    }
    return render(request, 'mainapp/index.html', context)


# @cache_page(3600)
# @never_cache
def products(request, page=1):
    # categories = ProductCategory.objects.all()
    # products_list = Product.objects.all()
    hot_product_pk = random.choice(Product.objects.filter(is_active=True).values_list('pk', flat=True))
    hot_product = get_product(hot_product_pk)
    same_products = hot_product.category.product_set.filter(is_active=True).select_related().exclude(pk=hot_product.pk)

    products_paginator = Paginator(same_products, 1)
    try:
        same_products = products_paginator.page(page)
    except PageNotAnInteger:
        same_products = products_paginator.page(1)
    except EmptyPage:
        same_products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Products',
        'categories': get_category_list(),
        # 'products': products_list[:3],
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/product-details.html', context)


def category_products(request, pk, page=1):
    # categories = ProductCategory.objects.all()
    if pk == '0':
        category = {'pk': 0, 'name': 'Все'}
        products_list_category = get_products()
    else:
        category = get_category(pk)
        products_list_category = get_products_in_productcategory(pk)

    products_paginator = Paginator(products_list_category, 3)
    try:
        products_list_category = products_paginator.page(page)
    except PageNotAnInteger:
        products_list_category = products_paginator.page(1)
    except EmptyPage:
        products_list_category = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'Products',
        'categories': get_category_list(),
        'products': products_list_category,
        'category': category,
    }
    return render(request, 'mainapp/category_products.html', context)


# @never_cache
def product_page(request, pk):
    # categories = ProductCategory.objects.all()
    product = get_product(pk)
    context = {
        'page_title': 'каталог',
        'categories': get_category_list(),
        'category': product.category,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)


# @cache_page(86400)
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
            product = get_product(pk)
            return JsonResponse({
                'product_price': product.price,
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })
