# login/views.py
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import *
from .form import *
from random import randint
from FM.settings import EMAIL_FROM
from django.contrib.auth.decorators import login_required
import base64
import face_recognition
import os


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
        print(username, password)
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
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            # if 'image' in request.FILES:
            #     user.image = request.FILES['image']
            user.save()
            user_info = UserProfile.objects.create(user=user)
            user_info.nickname = nickname
            user_info.gender = gender
            if 'avatar' in request.FILES:
                user_info.avatar = request.FILES['avatar']
            else:
                user_info.avatar = 'profile/default.jpg'
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
        photo = request.POST.get('hidden_photo', None)
        username = request.POST.get('username', None)
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return render(request, 'login_face.html', {'username': username, 'message': 'no existed'})
        print(user.image)
        if user.image == '':
            return render(request, 'login_face.html',
                          {'username': username, 'message': 'face login is not authorised'})
        if photo is not None and photo != '':
            print(photo)
            index = photo.find('base64,')
            base64Str = photo[index + 6:]
            unknown_face = base64.b64decode(base64Str)
            index = len(os.listdir('media/login'))
            path = 'media/login/'+str(index)+'.png'
            file = open(path, 'wb')
            file.write(unknown_face)
            file.close()
            unknown_face = face_recognition.load_image_file(path)
            #os.remove(path)
            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_face)[0]
            except IndexError:
                return render(request, 'login_face.html', {'username': username, 'message': 'no face detected'})
            known_face = face_recognition.load_image_file(user.image)
            known_face_encoding = face_recognition.face_encodings(known_face)[0]
            result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, 0.5)
            if result[0]:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/index/")
                else:
                    return render(request, 'login_face.html', {'username': username, 'message': 'user cannot be user'})
            else:
                return render(request, 'login_face.html', {'username': username, 'message': 'no macth'})
    return render(request, 'login_face.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def profilechange(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST,request.FILES)
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            if 'image' in request.FILES:
                image_path = request.FILES['image']
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_recognition.face_encodings(image)[0]
                    user.image = image_path
                    user.save()
                except IndexError:
                    form.initial['image'] = user.image
                    form.initial['avatar'] = user_profile.avatar
                    return render(request, 'profilechange.html', {'user_profile': user_profile, 'profile_form': form, 'message': ' photo : no face detected'})
            if 'avatar' in request.FILES:
                user_profile.__dict__.update(**form.cleaned_data)
                user_profile.avatar = request.FILES['avatar']
            else:
                avatar_path = user_profile.avatar
                user_profile.__dict__.update(**form.cleaned_data)
                user_profile.avatar = avatar_path
            user_profile.save()
            form.initial['image'] = user.image
            form.initial['avatar'] = user_profile.avatar
            return render(request, 'profilechange.html',
                          {'user_profile': user_profile, 'profile_form': form, 'message': "修改成功"})
    profile_form = ProfileForm(instance=user_profile)
    profile_form.initial['image'] = User.objects.get(username=request.user).image
    return render(request, 'profilechange.html', {'user_profile': user_profile, 'profile_form': profile_form})


@login_required
def passwordchange(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        button = request.POST.get('btn-state', None)
        email = request.user.email
        if button == 'email':
            state = send_email(email)
            return render(request, 'passwordchange.html', {'user_profile': user_profile})
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
                    return render(request, 'login.html', {'user_profile': user_profile, 'message': '修改成功'})
                else:
                    return render(request, 'passwordchange.html', {'user_profile': user_profile, 'message': '验证码错误'})
    return render(request, 'passwordchange.html', {'user_profile': user_profile})


@login_required
def accountcancellation(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return render(request, 'login.html')
    return render(request, 'accountcancellation.html', {'user_profile': user_profile})
