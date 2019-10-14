from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Goods, Comment, InstationMessage, Cart, Order
from user.models import UserProfile
from .forms import *
from django.db.models import Q


# Create your views here.

@login_required
def index(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        goods_list = Goods.objects.filter(
            Q(name__icontains=content) | Q(trade_location__icontains=content)).order_by('-publish_time')
        context_dic = {'user_profile': user_profile, 'goods': goods_list, 'message': content}
        return render(request, 'index.html', context_dic)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        goods_list = Goods.objects.all().order_by('-publish_time')
        context_dic = {'user_profile': user_profile, 'goods': goods_list}
        return render(request, 'index.html', context_dic)


@login_required
def index_category(request, category_id):
    user_profile = UserProfile.objects.get(user=request.user)
    category = Category.objects.get(id=category_id)
    goods_list = Goods.objects.filter(category=category).order_by('-publish_time')
    context_dic = {'user_profile': user_profile, 'goods': goods_list,'message':category.name}
    return render(request, 'index.html', context_dic)


@login_required
def about(request):
    return HttpResponse("Rongyi Li, Yingfei Li and Ying Chen 's assignments")


@login_required
def goods_page(request, goods_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    comment_form = CommentForm()
    goods = Goods.objects.get(pk=goods_id)
    comment_list = Comment.objects.filter(goods=goods).order_by('comment_time').reverse()
    context_dic = {'goods': goods, 'comments': comment_list, 'form': comment_form, 'user_profile': user_profile}
    return render(request, 'goods.html', context_dic)


@login_required
def add_comment(request, goods_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

            comment = comment_form.save(commit=True)
            goods = Goods.objects.get(pk=goods_id)
            user = UserProfile.objects.get(user=request.user)
            comment.user = user
            comment.goods = goods
            comment.save()

            message = InstationMessage()
            message.sender = user
            message.receiver = goods.seller
            message.content = comment.content
            message.save()

            return goods_page(request, goods_id)
        else:
            print(comment_form.errors)


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

        return goods_page(request, goods_id)


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
def mygoods(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.filter(seller=user_profile, name__icontains=content).reverse()
        return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods, 'message': content})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.filter(seller=user_profile).reverse()
        return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})


@login_required
def publish_goods(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        goods_form = GoodsForm(request.POST)
        if goods_form.is_valid():
            goods = goods_form.save(commit=True)
            goods.seller = user_profile
            if 'picture' in request.FILES:
                goods.picture = request.FILES['picture']
            goods.save()
            goods = Goods.objects.filter(seller=user_profile).reverse()
            return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})
        else:
            print(goods_form.errors)
    goods_form = GoodsForm()
    return render(request, 'publish_goods.html', {'user_profile': user_profile, 'form': goods_form})


@login_required
def edit_goods(request, goods_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        goods_form = GoodsForm(request.POST)
        if goods_form.is_valid():
            goods = Goods.objects.get(id=goods_id)
            goods.__dict__.update(**goods_form.cleaned_data)
            print(request.POST)
            if 'picture' in request.FILES:
                goods.picture = request.FILES['picture']
            else:
                goods.picture = request.POST['default_picture']
            goods.save()
            goods = Goods.objects.filter(seller=user_profile).reverse()
            return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})
    else:
        goods = Goods.objects.get(id=goods_id)
        goods_form = GoodsForm(instance=goods)
        return render(request, 'edit_goods.html', {'user_profile': user_profile, 'form': goods_form, 'goods': goods})


@login_required
def delete_goods(request, goods_id):
    if request.method == 'GET':
        if goods_id is not None:
            Goods.objects.filter(id=goods_id).delete()
        user_profile = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.filter(seller=user_profile).reverse()
        return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})


@login_required
def mysale(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(seller=user_profile, status=False).reverse()
    return render(request, 'mysale.html', {'user_profile': user_profile, 'orders': orders})


@login_required
def completesale(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(seller=user_profile, status=True).reverse()
    return render(request, 'completesale.html', {'user_profile': user_profile, 'orders': orders})


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


@login_required
def myorder(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(buyer=user_profile, status=False, goods__name__icontains=content).reverse()
        return render(request, 'myorder.html', {'user_profile': user_profile, 'orders': orders, 'message': content})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(buyer=user_profile, status=False).reverse()
        return render(request, 'myorder.html', {'user_profile': user_profile, 'orders': orders})


@login_required
def completeorder(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(buyer=user_profile, status=True, goods__name__icontains=content).reverse()
        return render(request, 'completeorder.html', {'user_profile': user_profile, 'orders': orders, 'message': content})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(buyer=user_profile, status=True).reverse()
        return render(request, 'completeorder.html', {'user_profile': user_profile, 'orders': orders})


@login_required
def check_order(request, order_id):
    user_profile = UserProfile.objects.get(user=request.user)
    order = Order.objects.get(id=order_id)
    order.status = True
    order.save()
    orders = Order.objects.filter(buyer=user_profile, status=True).reverse()
    return render(request, 'completeorder.html', {'user_profile': user_profile, 'orders': orders})


@login_required
def delete_order(request, order_id):
    user_profile = UserProfile.objects.get(user=request.user)
    Order.objects.filter(id=order_id).delete()
    orders = Order.objects.filter(buyer=user_profile, status=False).reverse()
    return render(request, 'myorder.html', {'user_profile': user_profile, 'orders': orders})


@login_required
def categories(request):
    user_profile = UserProfile.objects.get(user=request.user)
    Categories = Category.objects.all()
    return render(request, 'categories.html', {'user_profile': user_profile, 'categories': Categories})
