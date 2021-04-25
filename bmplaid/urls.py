"""bmplaid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from plaid_app.views import Bmplaid, link_page, AccountHandler, TransactionHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', link_page.as_view(), name="get-link"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('get_link_token/', Bmplaid.as_view(), name="token-genration"),
    path('get_access_token/', link_page.as_view(), name='public-token' ),
    path('account/', AccountHandler.as_view(), name='account' ),
    path('transaction/', TransactionHandler.as_view(), name='transaction')
]
