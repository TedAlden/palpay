"""
URL configuration for webapps2025 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path

from register import views as register_views
from payment import views as payment_views

urlpatterns = [
    path("", payment_views.home, name="home"),
    path("payment/", include("payment.urls")),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("register/", register_views.register_user, name="register"),
    path("login/", register_views.login_user, name="login"),
    path("logout/", register_views.logout_user, name="logout"),
]
