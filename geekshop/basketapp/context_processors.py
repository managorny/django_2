def basket(request):
    if request.user.is_authenticated:
        basket = request.user.basket.all()
    else:
        basket = []
    return {
        'basket': basket,
    }
