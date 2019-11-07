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
        print(request.POST)
        content = request.POST.get('search', '')
        option = request.POST.get('option', None)
        user_profile = UserProfile.objects.get(user=request.user)
        categories = Category.objects.all()
        if option is None or option == 'all':
            goods_list = Goods.objects.filter(Q(checked=True),
                                              Q(name__icontains=content) | Q(trade_location__icontains=content)).order_by('-publish_time')
        else:
            goods_list = Goods.objects.filter(Q(checked=True),
                                              Q(category__name=option) & Q(name__icontains=content)).order_by(
                '-publish_time')
            content = option + '+' + content
        context_dic = {'user_profile': user_profile, 'goods': goods_list, 'message': content, 'categories': categories}
        return render(request, 'index.html', context_dic)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        goods_list = Goods.objects.filter(checked=True).order_by('-publish_time')
        categories = Category.objects.all()
        context_dic = {'user_profile': user_profile, 'goods': goods_list, 'categories': categories}
        return render(request, 'index.html', context_dic)


@login_required
def index_category(request, category_id):
    user_profile = UserProfile.objects.get(user=request.user)
    category = Category.objects.get(id=category_id)
    goods_list = Goods.objects.filter(category=category).order_by('-publish_time')
    categories = Category.objects.all()
    context_dic = {'user_profile': user_profile, 'goods': goods_list, 'message': category.name,
                   'categories': categories}
    return render(request, 'index.html', context_dic)


@login_required
def about(request):
    return HttpResponse("Rongyi Li, Yingfei Li and Ying Chen 's assignments")


@login_required
def categories(request):
    user_profile = UserProfile.objects.get(user=request.user)
    Categories = Category.objects.all()
    return render(request, 'categories.html', {'user_profile': user_profile, 'categories': Categories})
