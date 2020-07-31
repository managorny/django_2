from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderForm, OrderItemForm


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class OrderList(PageTitleMixin, ListView):
    model = Order
    page_title = 'Список заказов'

    def get_queryset(self):
        return self.request.user.order_set.all()
        # return Order.objects.filter(user=self.request.user)


class OrderCreate(PageTitleMixin, CreateView):
    model = Order
    form_class = OrderForm
    page_title = 'Создание заказа'
    success_url = reverse_lazy('ordersapp:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = order_form_set(self.request.POST, self.request.FILES)
        else:
            basket_items = self.request.user.basket.all()
            if len(basket_items):
                order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = order_form_set()

                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
            else:
                formset = order_form_set()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(PageTitleMixin, UpdateView):
    model = Order
    form_class = OrderForm
    page_title = 'Редактирование заказа'
    success_url = reverse_lazy('ordersapp:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1
        )
        if self.request.POST:
            formset = OrderFormSet(
                self.request.POST, self.request.FILES,
                instance=self.object
            )
        else:
            formset = OrderFormSet(instance=self.object)
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:index')


class OrderDetail(PageTitleMixin, DetailView):
    model = Order
    page_title = "Просмотр заказа"


def order_preparing_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_FOR_ASSEMBLY
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:index'))
