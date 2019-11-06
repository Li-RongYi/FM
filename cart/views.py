from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from goods.models import Goods,Comment
from order.models import Order
from goods.forms import CommentForm
from .models import Cart


# Create your views here.
@login_required
def cart(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        carts = Cart.objects.filter(user=user_profile, goods__name__icontains=content).reverse()
        return render(request, 'cart.html', {'user_profile': user_profile, 'carts': carts, 'message': content})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        carts = Cart.objects.filter(user=user_profile).reverse()
        return render(request, 'cart.html', {'user_profile': user_profile, 'carts': carts})


@login_required
def add_cart(request, goods_id):
    if request.method == 'POST':
        cart = Cart.objects.create()
        cart.user = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.get(pk=goods_id)
        cart.goods = goods
        cart.price = goods.price
        num = int(request.POST.get("quantity_input", 1))
        cart.num = num
        cart.sum = num * cart.price
        cart.save()

        user_profile = UserProfile.objects.get(user=request.user)
        comment_form = CommentForm()
        goods = Goods.objects.get(pk=goods_id)
        comment_list = Comment.objects.filter(goods=goods).order_by('comment_time').reverse()
        context_dic = {'goods': goods, 'comments': comment_list, 'form': comment_form, 'user_profile': user_profile}
        return render(request, 'goods.html', context_dic)


@login_required
def clear_cart(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        Cart.objects.filter(user=user_profile).delete()
        return render(request, 'cart.html', {'user_profile': user_profile})


@login_required
def delete_cart(request, cart_id):
    if request.method == 'GET':
        if cart_id is not None:
            Cart.objects.filter(id=cart_id).delete()
        user_profile = UserProfile.objects.get(user=request.user)
        carts = Cart.objects.filter(user=user_profile)
        return render(request, 'cart.html', {'user_profile': user_profile, 'carts': carts})

@login_required
def checkout(request, cart_id):
    user_profile = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        order = Order.objects.create()
        cart = Cart.objects.get(id=cart_id)
        order.seller = cart.goods.seller
        order.buyer = user_profile
        order.goods = cart.goods
        order.num = cart.num
        order.sum = cart.sum
        order.contact = request.POST['contact']
        order.message = request.POST['message']
        order.save()
        Cart.objects.filter(id=cart_id).delete()
        orders = Order.objects.filter(buyer=user_profile, status=False)
        return render(request, 'myorder.html', {'user_profile': user_profile, 'orders': orders})
    return render(request, 'checkout.html', {'user_profile': user_profile, 'cart': cart})