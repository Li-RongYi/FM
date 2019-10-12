# login/views.py
from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import *
from .form import *
from random import randint
from FM.settings import EMAIL_FROM
from django.contrib.auth.decorators import login_required
import base64


def authenticate(username=None, password=None):
    try:
        user = User.objects.get(Q(email=username) | Q(username=username))
        if user.check_password(password):
            return user

    except User.DoesNotExist:
        return None


def send_email(email):
    code = ''
    for _ in range(6):
        code += str(randint(0, 9))

    msg = "验证码: " + code
    title = "二手交易系统"
    try:
        send_mail(title, msg, EMAIL_FROM, [email])
        obj, created = ConfirmString.objects.get_or_create(email=email)
        obj.code = code
        obj.save()
        return True
    except:
        return False


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username,password)
        message = '账号或者密码错误'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:  # 是否是可用的。对于一些想要删除账号的数据，我们设置这个值为0就可以了，而不是真正的从数据库中删除。
                login(request, user)
                return HttpResponseRedirect("/index/")  # HttpResponse("登录成功")
            else:
                message = '账户无法使用'
        return render(request, 'login.html', {'username': username, 'message': message})
    return render(request, 'login.html')


def register_info(request, username='12345'):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        if register_form.is_valid():
            password = register_form.cleaned_data['password1']
            nickname = register_form.cleaned_data['nickname']
            gender = register_form.cleaned_data['gender']
            avatar = register_form.cleaned_data['avatar']
            image = register_form.cleaned_data['image']
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.image = image
            user.save()
            user_info = UserProfile.objects.create(user=user)
            user_info.nickname = nickname
            user_info.gender = gender
            user_info.avatar = avatar
            user_info.save()

            return render(request, 'login.html', {'username': username})
        else:
            return render(request, 'register_info.html',
                          {'username': username, 'email': email, 'register_form': register_form, 'message': 'error'})
    return render(request, 'register_info.html', {'username': username, 'register_form': RegisterForm()})


def register(request):
    def new_username():
        username = ''
        for _ in range(10):
            username += str(randint(0, 9))

        while User.objects.filter(username=username):
            username = ''
            for _ in range(10):
                username += str(randint(0, 9))
        return username

    if request.method == "POST":
        email = request.POST.get('email', None)
        button = request.POST.get('btn-state', None)
        if User.objects.filter(email=email):
            return render(request, 'register.html', {'email': email, 'message': '邮箱已存在'})
        if button == 'email':
            state = send_email(email)
            if state:
                return render(request, 'register.html', {'email': email, 'message': '请前往邮箱获取验证码'})
            else:
                return render(request, 'register.html', {'email': email, 'message': '邮箱错误'})
        else:
            if ConfirmString.objects.filter(email=email):
                confirmcode = ConfirmString.objects.get(email=email).__dict__['code']
                code = request.POST.get('code', None)
                if confirmcode == code:
                    ConfirmString.objects.filter(email=email).delete()
                    username = new_username()
                    return render(request, 'register_info.html',
                                  {'username': username, 'email': email, 'register_form': RegisterForm()})
    return render(request, 'register.html')


def login_code(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        button = request.POST.get('btn-state', None)
        if not User.objects.filter(email=email):
            return render(request, 'login_code.html', {'email': email, 'message': '邮箱未注册'})
        if button == 'email':
            state = send_email(email)
            if state:
                return render(request, 'login_code.html', {'email': email, 'message': '请前往邮箱获取验证码'})
            else:
                return render(request, 'login_code.html', {'email': email, 'message': '邮箱错误'})
        else:
            if ConfirmString.objects.filter(email=email):
                confirmcode = ConfirmString.objects.get(email=email).__dict__['code']
                code = request.POST.get('code', None)
                if confirmcode == code:
                    ConfirmString.objects.filter(email=email).delete()
                    user = User.objects.get(email=email)
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/index/")
                    else:
                        return render(request, 'login_code.html', {'email': email, 'message': '账户无法使用'})
            return render(request, 'login_code.html', {'email': email, 'message': '邮箱或者验证码错误'})
    else:
        return render(request, 'login_code.html')


def login_face(request):
    if request.method == 'POST':
        print(request.POST)
        photo = request.POST.get('hidden_photo',None)
        if photo is not None:
            img = base64.b64decode(photo.split(',')[-1])
    return render(request, 'login_face.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def profilechange(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        pass #save  all infomation

    return render(request,'profilechange.html', {'user_profile':user_profile,'profile_form':ProfileForm()})

@login_required
def passwordchange(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        button = request.POST.get('btn-state', None)
        email = request.user.email
        if button == 'email':
            state = send_email(email)
            return render(request, 'passwordchange.html',{'user_profile':user_profile})
        else:
            if ConfirmString.objects.filter(email=email):
                confirmcode = ConfirmString.objects.get(email=email).__dict__['code']
                code = request.POST.get('code', None)
                if confirmcode == code:
                    ConfirmString.objects.filter(email=email).delete()
                    password = request.POST.get('newpassword1', None)
                    user = User.objects.get(username=request.user)
                    user.set_password(password)
                    user.save()
                    return render(request, 'login.html', {'user_profile':user_profile,'message': '修改成功'})
                else:
                    return render(request, 'passwordchange.html', {'user_profile':user_profile,'message': '验证码错误'})
    return render(request,'passwordchange.html',{'user_profile':user_profile})

@login_required
def accountcancellation(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return render(request, 'login.html')
    return render(request,'accountcancellation.html',{'user_profile':user_profile})


