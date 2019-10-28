from django import forms
from .models import UserProfile


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    nickname = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='性别', choices=gender)
    #image = forms.ImageField(label='照片',required=False)
    avatar = forms.ImageField(label='头像',required=False)

class ProfileForm(forms.ModelForm):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    nickname = forms.CharField(label="昵称", max_length=128)
    gender = forms.ChoiceField(label='性别', choices=gender)
    contact = forms.CharField(label='联系', max_length=20, required=False)
    avatar = forms.ImageField(label='头像',required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)
