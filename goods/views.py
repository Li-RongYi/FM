from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Goods, Comment, InstationMessage
from user.models import UserProfile
from order.models import Order
from .forms import *


# Create your views here.


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

            # message = InstationMessage()
            # message.sender = user
            # message.receiver = goods.seller
            # message.content = comment.content
            # message.save()

            user_profile = UserProfile.objects.get(user=request.user)
            comment_form = CommentForm()
            goods = Goods.objects.get(pk=goods_id)
            comment_list = Comment.objects.filter(goods=goods).order_by('comment_time').reverse()
            context_dic = {'goods': goods, 'comments': comment_list, 'form': comment_form, 'user_profile': user_profile}
            return render(request, 'goods.html', context_dic)
        else:
            print(comment_form.errors)


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
            print(request.POST)
            if 'picture' in request.FILES:
                goods.__dict__.update(**goods_form.cleaned_data)
                goods.picture = request.FILES['picture']
            else:
                picture = goods.picture
                goods.__dict__.update(**goods_form.cleaned_data)
                goods.picture = picture
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
