from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

def checkout(request):
    cart = Cart(request)
    # Eğer sepet boşsa, kullanıcıyı ana sayfaya yönlendir
    if not cart:
        return redirect('pages:home')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['variant'].product,
                    variant=item['variant'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:payment_process'))
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['email'] = request.user.email
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

def payment_process(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('pages:home')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/process.html', {'order': order})

def payment_done(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('pages:home')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    # Sipariş tamamlandıktan sonra session'dan order_id'yi temizle
    if 'order_id' in request.session:
        del request.session['order_id']
    return render(request, 'orders/done.html', {'order_id': order_id})

def payment_canceled(request):
    return render(request, 'orders/canceled.html')

@login_required
def order_history(request):
    orders = request.user.order_set.all()
    return render(request, 'orders/history.html', {'orders': orders})