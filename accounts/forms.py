# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class EditAcc(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'bio', 'status', 'profpic')


class DoComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description','comentpost')


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment here !',
            'rows': 4,
            'cols': 50
        }))

    class Meta:
        model = Comment
        fields = ['description']
