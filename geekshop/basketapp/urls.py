from django.urls import path, re_path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('<int:page>/', basketapp.index, name='index_pagination'),
    re_path(r'add/product/(?P<pk>\d+)/', basketapp.add_product, name="add_product"),
    # path('add/product/<int:pk>'/, basketapp.add_product, name="add_product"),
    re_path(r'delete/product/(?P<pk>\d+)/', basketapp.delete_product, name="delete_product"),
    re_path(r'^change/(?P<pk>\d+)/quantity/(?P<quantity>\d+)/$', basketapp.change),
]
