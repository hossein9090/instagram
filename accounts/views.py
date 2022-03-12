from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from accounts.models import Account, Post, Follow, Comment, Likes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, EditAcc, DoComment
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


class t(TemplateView):
    template_name = 'accounts/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = [
            {
                'id': obj.id,
                'value': obj.user.id,
                'date': obj.status,
            }
            for obj in Account.objects.all()
        ]

        return context


# class SomeTemplateView(TemplateView):
#     template_name = 'accounts/temview.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['data'] = [
#             {
#                 'id': obj.id,
#                 'value': obj.user,
#                 'date': obj.status,
#             }
#             for obj in Account.objects.all()
#         ]
#
#         return context


def showprofile(request):
    us = request.user
    inuser = request.user.id
    account_qs = Account.objects.all()
    post_qs = Post.objects.filter(account_id=inuser)
    follower = len(Follow.objects.filter(profile__user=us, verify=True))
    following = len(Follow.objects.filter(user=us, verify=True))
    post = len(Post.objects.filter(account__user=us))

    context = {
        "account_qs": account_qs,
        "post_qs": post_qs,
        "inuser": inuser,
        "follower": follower,
        "following": following,
        "post": post,
    }
    return render(request, "accounts/testpack.html", context)


def showsearchingprofile(request, id):
    tu = request.user
    account_qs = Account.objects.filter(id=id)
    post_qs = Post.objects.filter(account_id=id)
    v_followe = Follow.objects.filter(user=request.user, profile_id=id).first()
    follower = len(Follow.objects.filter(profile_id=id, verify=True))
    following = len(Follow.objects.filter(user__accuser=id))
    context = {
        "account_qs": account_qs,
        "post_qs": post_qs,
        "follower": follower,
        "following": following,
        "tu": tu,
        "v_followe": v_followe
    }
    return render(request, "accounts/showsearchprofile.html", context)


def showfriendpost(request):
    tu = request.user
    auser = request.user
    profiles_qs = Follow.objects.filter(user=auser)
    # for q in profiles_qs:
    #     s = q.profile.accountpost.all()

    context = {
        "profiles_qs": profiles_qs,
        "tu": tu
    }

    return render(request, "accounts/friendspost.html", context)


def doingfollow(request, id):
    accuont = Account.objects.filter(id=id).first()
    check = Follow.objects.filter(user=request.user, profile_id=id).exists()
    if check:
        return HttpResponse('shoma in shakhs ro follow kardi')
    elif accuont.status == 'public':
        Follow.objects.create(user=request.user, profile_id=id, verify=True)
        return HttpResponse('follow shod')
    elif accuont.status == 'private':
        Follow.objects.create(user=request.user, profile_id=id, verify=False)
        return HttpResponse('darkhast e follow ersal shod')


def unfollow(request, id):
    Follow.objects.filter(user=request.user, profile_id=id).delete()
    return HttpResponse('unfollow shodesh')


def show_follow_req(request):
    req = Follow.objects.filter(profile__user=request.user, verify=False)
    context = {
        "req": req,
    }
    return render(request, "accounts/show_follow_req.html", context)


def verify_follow_req(request, id):
    req = Follow.objects.filter(profile__user=request.user, user_id=id).first()
    print(req)
    req.verify = True
    req.save()
    return HttpResponse('ok shod')


def show_follower(request):
    follower = Follow.objects.filter(profile__user=request.user, verify=True)
    context = {
        "follower": follower,
    }
    return render(request, "accounts/follower.html", context)


def show_following(request):
    following = Follow.objects.filter(user=request.user, verify=True)
    context = {
        "following": following,
    }
    return render(request, "accounts/following.html", context)


def dolike(request, id):
    check = Likes.objects.filter(user=request.user, post_id=id).exists()
    if check:
        return HttpResponse('shoma in post ro like kardi')
    else:
        Likes.objects.create(user=request.user, post_id=id)
        return HttpResponse('like shod')


def unlike(request, id):
    Likes.objects.filter(user=request.user, post_id=id).delete()
    return HttpResponse('unlike shodesh')


def search(request):
    user_search_qs = User.objects.filter(username__icontains=request.GET.get('q', ''))
    return render(request, "accounts/search2.html", {"users_finder": user_search_qs})


def searching(request):
    return render(request, "accounts/search.html")


def settings(request):
    return render(request, "accounts/settings.html")


def test(request):
    us = request.user
    inuser = request.user.id
    account_qs = Account.objects.all()
    post_qs = Post.objects.filter(account_id=inuser)
    follower = len(Follow.objects.filter(profile__user=us, verify=True))
    following = len(Follow.objects.filter(user=us, verify=True))
    post = len(Post.objects.filter(account__user=us))
    context = {
        "account_qs": account_qs,
        "post_qs": post_qs,
        "inuser": inuser,
        "follower": follower,
        "following": following,
        "post": post,
    }
    return render(request, "accounts/profile.html", context)


#################### index#######################################
def index(request):
    return render(request, 'accounts/index.html', {'title': 'index'})


########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('accounts/Email.html')
            d = {'username': username}
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'title': 'reqister here'})


################ login forms###################################################
def Login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'title': 'log in'})


#
# class RegisterView(CreateView):
#     template_name = "registration/register.html"
#     form_class = RegisterForm
#     success_url = '/login'

@login_required()
def edit_acc(request):
    if request.method == 'POST':
        form = EditAcc(request.POST, instance=request.user.accuser)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/editprofile.html')
    else:
        form = EditAcc(instance=request.user.accuser)
    return render(request, 'accounts/editprofile.html', {'form': form})


from .forms import CommentForm


def post_detailview(request, id):
    post = Post.objects.filter(id=id).first()
    target_acc = request.user
    if request.method == 'POST':
        # cf = CommentForm(request.POST or None)
        # if cf.is_valid():
        content = request.POST.get('comment')
        comment = Comment.objects.create(comentpost=post, user=target_acc, description=content)
        comment.save()
        return HttpResponse('comment sabt shod')
    else:
        cf = CommentForm()

    context = {
        'comment_form': cf,
        'post_id': id
    }
    return render(request, 'accounts/post_detail.html', context)


def delet_comment(request, id):
    Comment.objects.filter(user=request.user, id=id).delete()
    return HttpResponse('comment delet shod')

# def docomment(request, id):
#     current_user = request.user
#     select_post = Post.objects.filter(id=id).first()
