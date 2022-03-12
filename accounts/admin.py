from django.contrib import admin

from .models import Account, Follow, Post, Comment, Likes

admin.site.register(Account)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Likes)


