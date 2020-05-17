from django.shortcuts import render, redirect, reverse
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.paid = True
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return render(request, 'order/payment.html',
                          {'email': order.email, 'amount': cart.get_total_price_after_discount() * 100})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})










