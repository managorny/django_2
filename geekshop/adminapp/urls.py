from django.urls import path, re_path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.ShopUserList.as_view(), name='index'),
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('category/list/', adminapp.CategoriesListView.as_view(), name='categories'),
    path('category/list/<int:page>/', adminapp.CategoriesListView.as_view(), name="categories_pagination"),
    path('category/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    re_path(r'^category/(?P<pk>\d+)/products_list/$', adminapp.CategoryProductsListView.as_view(),
            name='category_products_list'),
    path('category/<int:pk>/products_list/<int:page>/', adminapp.CategoryProductsListView.as_view(),
         name="category_products_list_pagination"),

    # TODO: сделать проброс category_id
    path('category/product/create/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('product/read/<int:pk>/', adminapp.ProductDetail.as_view(), name='product_read'),

    path('product/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

    # path('', adminapp.index, name='index'),
    # path('user/create/', adminapp.user_create, name='user_create'),
    # path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    # path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    # path('category/list/', adminapp.categories, name='categories'),
    # path('category/list/<int:page>/', adminapp.categories, name="categories_pagination"),
    # path('category/create/', adminapp.category_create, name='category_create'),
    # path('category/update/<int:pk>/', adminapp.category_update, name='category_update'),
    # path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    # path('category/<int:pk>/products_list/', adminapp.category_products_list, name='category_products_list'),
    # path('category/<int:pk>/products_list/<int:page>/', adminapp.category_products_list,
    #      name="category_products_list_pagination"),
    # path('category/<int:category_pk>/product/create/', adminapp.product_create, name='product_create'),
    # path('product/read/<int:pk>/', adminapp.product_read, name='product_read'),
    # path('product/update/<int:pk>/', adminapp.product_update, name='product_update'),
    # path('product/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]
