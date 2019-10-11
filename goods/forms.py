from django import forms
from django.contrib.auth.models import User
from .models import Category, Goods, Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=128,
                              widget=forms.Textarea(
                                  attrs={'id': 'comment_input', 'class': 'review_form_text', 'placeholder': "Message"}))

    class Meta:
        model = Comment
        fields = ('content',)


class GoodsForm(forms.ModelForm):
    name = forms.CharField(max_length=32, help_text="商品名称",
                           widget=forms.TextInput(attrs={'class': 'name', 'placeholder': '最多二十五个字'}))
    description = forms.CharField(max_length=512, help_text="商品详情", widget=forms.Textarea(
        attrs={'id': 'desc', 'placeholder': '建议填写物品用途、新旧程度、原价等信息，至少15个字'}))
    trade_location = forms.CharField(max_length=32, help_text="交易地点",
                                     widget=forms.TextInput(attrs={'id': 'trade_place', 'placeholder': '宿舍、金三角、食堂等'}))
    price = forms.FloatField(help_text="价格", widget=forms.TextInput(attrs={'id': 'price'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'id': 'contact'}), max_length=20)
    picture = forms.ImageField(help_text='照片', required=False)
    quantity = forms.IntegerField(help_text='数量')

    class Meta:
        model = Goods
        exclude = ('seller', 'picture_url')
