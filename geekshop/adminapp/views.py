from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from authapp.models import ShopUser
from mainapp.models import Product
from mainapp.models import ProductCategory
from adminapp.forms import AdminShopUserCreateForm
from adminapp.forms import AdminShopUserUpdateForm
from adminapp.forms import AdminProductCategoryUpdateForm
from adminapp.forms import AdminProductUpdateForm


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class ShopUserList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser
    page_title = 'Админка'


class UserCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    form_class = AdminShopUserCreateForm
    page_title = 'Создать пользователя'


class UserUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    form_class = AdminShopUserUpdateForm
    page_title = 'Редактирование пользователя'


class UserDeleteView(SuperUserOnlyMixin, DeleteView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    page_title = 'Удаление пользователя'    # TODO: проверить почему не работает

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'Админка/категории'
    paginate_by = 2


class CategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'Категории продуктов/Создание'


class CategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'Категории продуктов/Редактирование'


class CategoryDeleteView(SuperUserOnlyMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'Категории продуктов/Удаление'    # TODO: проверить почему не работает

    # TODO: сделать удаление/скрытие каскадом, чтобы товары этой категории также были скрыты при ее удалении
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryProductsListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = Product
    # category = model.objects.all()[0].category
    # page_title = f'категория {category.name}/продукты'    # TODO: сделать получение имени категории
    paginate_by = 2
    # TODO: сделать проброс category_id
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category_id'] = Product.objects.get(category_id=pk)
    #     return context


# TODO: сделать проброс category_id
class ProductCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = Product
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductUpdateForm
    page_title = 'Создание продукта'


class ProductUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminProductUpdateForm
    page_title = 'Продукты/редактирование'


class ProductDeleteView(SuperUserOnlyMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'Продукты/Удаление'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetail(DetailView):
    model = Product
    pk_url_kwarg = 'pk'     # product_pk


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     context = {
#         'title': 'Админка',
#         'object_list': users_list
#     }
#     return render(request, 'adminapp/index.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = AdminShopUserCreateForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserCreateForm()
#
#     context = {
#         'title': 'Создать пользователя',
#         'form': user_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def user_update(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('my_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'title': 'Редактирование пользователя',
#         'form': user_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def user_delete(request, pk):
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('my_admin:index'))
#
#     context = {
#         'title': 'Удаление пользователя',
#         'user_to_delete': user,
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def categories(request, page=1):
#     categories = ProductCategory.objects.all()
#
#     products_paginator = Paginator(categories, 2)
#     try:
#         categories = products_paginator.page(page)
#     except PageNotAnInteger:
#         categories = products_paginator.page(1)
#     except EmptyPage:
#         categories = products_paginator.page(products_paginator.num_pages)
#
#     context = {
#         'title': 'Админка/категории',
#         'object_list': categories,
#     }
#     return render(request, 'adminapp/productcategory_list.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = AdminProductCategoryUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminProductCategoryUpdateForm()
#
#     context = {
#         'title': 'Категории продуктов/Создание',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_update(request, pk):
#     obj = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductCategoryUpdateForm(request.POST, request.FILES, instance=obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminProductCategoryUpdateForm(instance=obj)
#
#     context = {
#         'title': 'Категории продуктов/Редактирование',
#         'form': form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_delete(request, pk):
#     obj = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         obj.is_active = False
#         obj.save()
#         return HttpResponseRedirect(reverse('my_admin:categories'))
#
#     context = {
#         'title': 'Категории продуктов/Удаление',
#         'object': obj,
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_products_list(request, pk, page=1):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     object_list = category.product_set.all()
#
#     products_paginator = Paginator(object_list, 2)
#     try:
#         object_list = products_paginator.page(page)
#     except PageNotAnInteger:
#         object_list = products_paginator.page(1)
#     except EmptyPage:
#         object_list = products_paginator.page(products_paginator.num_pages)
#
#     context = {
#         'title': f'категория {category.name}/продукты',
#         'category': category,
#         'object_list': object_list
#     }
#     return render(request, 'adminapp/category_products_list.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, category_pk):
#     category = get_object_or_404(ProductCategory, pk=category_pk)
#     if request.method == 'POST':
#         form = AdminProductUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'my_admin:category_products_list',
#                 kwargs={'pk': category.pk}
#             ))
#     else:
#         form = AdminProductUpdateForm(
#             initial={
#                 'category': category,
#                 # 'quantity': 10,
#                 # 'price': 157.9,
#             }
#         )
#
#     context = {
#         'title': 'продукты/создание',
#         'form': form,
#         'category': category,
#     }
#     return render(request, 'adminapp/product_update.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     obj = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': 'продукты/подробнее',
#         'object': obj,
#     }
#     return render(request, 'adminapp/product_read.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = AdminProductUpdateForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'my_admin:category_products_list',
#                 kwargs={'pk': product.category.pk}
#             ))
#     else:
#         form = AdminProductUpdateForm(instance=product)
#
#     context = {
#         'title': 'продукты/редактирование',
#         'form': form,
#         'category': product.category,
#     }
#     return render(request, 'adminapp/product_update.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     obj = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         obj.is_active = False
#         obj.save()
#         return HttpResponseRedirect(reverse(
#             'my_admin:category_products_list',
#             kwargs={'pk': obj.category.pk}
#         ))
#
#     context = {
#         'title': 'продукты/удаление',
#         'object': obj,
#     }
#     return render(request, 'adminapp/product_delete.html', context)
