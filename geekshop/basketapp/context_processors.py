def basket(request):
    if request.user.is_authenticated:
        # basket = request.user.basket.select_related().all()
        # print(basket.query)
        basket = request.user.basket.select_related('product', 'product__category').all()

    else:
        basket = []
    return {
        'basket': basket,
    }
