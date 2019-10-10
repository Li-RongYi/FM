from django import forms
from django.contrib.auth.models import User
from .models import Category, Goods, Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=128,
                              widget=forms.Textarea(attrs={'id': 'comment_input', 'class': 'review_form_text', 'placeholder': "Message" }))

    class Meta:
        model = Comment
        fields = ('content',)
