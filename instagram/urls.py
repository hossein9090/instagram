# from django.contrib import admin
# from django.urls import path, include
# from accounts.views import RegisterView
# # from registration import views as v
# # from account import views as user_view
# from django.contrib.auth import views as auth
#
# from django.conf.urls.static import static
# from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('account/', include("account.urls")),
#     path('', include("django.contrib.auth.urls")),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('accounts/', include("accounts.urls")),
#     # path("registration/", v.registration, name="registration"),
#
# ]
# if settings.DEBUG:
#     urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from accounts import views as user_view
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    ##### user related path##########################
    path('', include('accounts.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='accounts/index.html'), name='logout'),
    path('register/', user_view.register, name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
