from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.models import UserProfile
from goods.models import Goods
from .models import Category


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
    context_dic = {'user_profile': user_profile, 'goods': goods_list, 'message': category.name}
    return render(request, 'index.html', context_dic)


@login_required
def about(request):
    return HttpResponse("Rongyi Li, Yingfei Li and Ying Chen 's assignments")


@login_required
def categories(request):
    user_profile = UserProfile.objects.get(user=request.user)
    Categories = Category.objects.all()
    return render(request, 'categories.html', {'user_profile': user_profile, 'categories': Categories})
