from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('allauth.urls')),  # Required for login/signup/logout
    path('accounts/', include('django.contrib.auth.urls')),

]