from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),

    path('', views.home, name='home'),
    path('api/v1/', include('authentication.urls')),

    path('', include('brands.urls')),
    path('', include('categories.urls')),
    path('', include('suppliers.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path('', include('products.urls')),
    path('api/v1/', include('authentication.urls')),
]
