from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Goods, Comment, InstationMessage, Cart
from user.models import UserProfile
from .forms import *



# Create your views here.

@login_required
def index(request):
    # if request.user.is_authenticated:
    user_profile = UserProfile.objects.get(user=request.user)
    message_unread = InstationMessage.objects.filter(receiver=user_profile, active=True).count()
    category_list = Category.objects.all()
    goods_list = Goods.objects.all().order_by('-publish_time')
    context_dic = {'categories': category_list, 'user_profile': user_profile, 'goods': goods_list,
                   'message_unread': message_unread}
    return render(request, 'index.html', context_dic)


@login_required
def about(request):
    return HttpResponse("This is about page.")


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
    user_profile = UserProfile.objects.get(user=request.user)
    carts = Cart.objects.filter(user=user_profile)
    return render(request, 'cart.html',{'user_profile':user_profile,'carts':carts})

@login_required
def add_cart(request, goods_id):
    if request.method == 'POST':
        cart = Cart.objects.create()
        cart.user = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.get(pk=goods_id)
        cart.goods = goods
        num = int(request.POST.get("quantity_input",1))
        cart.num =num
        cart.sum =num*goods.price
        cart.save()

        return goods_page(request, goods_id)

@login_required
def clear_cart(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        Cart.objects.filter(user=user_profile).delete()
        return render(request, 'cart.html', {'user_profile': user_profile})


@login_required
def delete_cart(request,cart_id):
    if request.method == 'GET':
        if cart_id is not None:
            Cart.objects.filter(id=cart_id).delete()
        user_profile = UserProfile.objects.get(user=request.user)
        carts = Cart.objects.filter(user=user_profile)
        return render(request, 'cart.html', {'user_profile': user_profile, 'carts': carts})


@login_required
def mygoods(request):
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
            print(goods.picture)
            if 'picture' in request.FILES:
                goods.picture = request.FILES['picture']
            goods.save()
            goods = Goods.objects.filter(seller=user_profile).reverse()
            return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})
        else:
            print(goods_form.errors)
    goods_form = GoodsForm()
    return render(request, 'publish_goods.html', {'user_profile': user_profile,'form': goods_form})

@login_required
def edit_goods(request,goods_id):
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
        return render(request, 'edit_goods.html', {'user_profile': user_profile,'form': goods_form,'goods': goods})

@login_required
def delete_goods(request,goods_id):
    if request.method == 'GET':
        if goods_id is not None:
            Goods.objects.filter(id=goods_id).delete()
        user_profile = UserProfile.objects.get(user=request.user)
        goods = Goods.objects.filter(seller=user_profile).reverse()
        return render(request, 'mygoods.html', {'user_profile': user_profile, 'goods': goods})



