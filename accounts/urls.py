# from django.urls import path
#
# from accounts.views import RegisterView
# from .views import test, showprofile
# # from account import views as user_view
# from django.contrib.auth import views as auth
#
# urlpatterns = [
#     path('profile/', showprofile, name='showprofile'),
#     # path('profile/', test, name='test'),
#     path('register/', RegisterView.as_view(), name='register_class'),
# ]


from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
    path('accounts/profile/', views.showprofile, name='showprofile'),
    path('accounts/showfriendpost/', views.showfriendpost, name='showfriendpost'),
    path('doingfollow/<str:tu>', views.doingfollow, name='doingfollow'),######################
    path('showsearchingprofile/<int:id>', views.showsearchingprofile, name='showsearchingprofile'),######################
    path('accounts/settings/', views.settings, name='settings'),
    # path('blogpost-like/<int:pk>', views.BlogPostLike, name='blogpost_like'),
    path('search/', views.search, name='search'),
    path('searching/', views.searching, name='searching'),
    path('showprofl/<int:pk>', views.test, name='showprofl'),
    path('editacc/', views.edit_acc, name='editacc'),
    # path('docomment/<int:id>/<int:comment_id>', views.docomment, name='docomment'),
    path('follow/<int:id>', views.doingfollow, name='doingfollow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('like/<int:id>', views.dolike, name='dolike'),
    path('unlike/<int:id>', views.unlike, name='unlike'),
    path('post_detailview/<int:id>', views.post_detailview, name='post_detailview'),
    path('delet_comment/<int:id>', views.delet_comment, name='delet_comment'),
    path('show_follower/', views.show_follower, name='show_follower'),
    path('show_following/', views.show_following, name='show_following'),
    path('show_follow_req/', views.show_follow_req, name='show_follow_req'),
    path('verify_follow_req/<int:id>', views.verify_follow_req, name='verify_follow_req'),
    path('t/', views.t.as_view(), name='t'),
]
