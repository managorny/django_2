from django.urls import path, re_path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name="index"),
    path('products/', mainapp.products, name="products"),
    path('products/<int:page>/', mainapp.products, name="same_products_pagination"),
    re_path(r'^category/(?P<pk>\d+)/products/$', mainapp.category_products, name="category_products"),
    # path(r'category/<int:pk>/products/', mainapp.category_products, name="category_products"),
    re_path(r'^category/(?P<pk>\d+)/products/(?P<page>\d+)/$', mainapp.category_products,
            name="category_products_pagination"),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product_page, name='product_page'),
    path('contacts/', cache_page(86400)(mainapp.contacts), name="contacts"),

    re_path(r'^product/detail/(?P<pk>\d+)/async/$', mainapp.product_detail_async),
]
