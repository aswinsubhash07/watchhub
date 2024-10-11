"""
URL configuration for WatchHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from watch import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path("",views.SignInView.as_view(),name="login"),

    path("register/",views.SignUpView.as_view(),name="register"),

    path("signout/",views.SignOutView.as_view(),name="logout"),

    path("home/",views.HomeView.as_view(),name="home"),

    path("project/deatil/<int:pk>/",views.ProjectDetailView.as_view(),name="project-detail"),

    path("project/add/wishlist/<int:pk>",views.AddtoCartView.as_view(),name="add-cart"),

    path("wishlist/items/",views.WishListView.as_view(),name="wish-list"),

    path("wishlist/remove/<int:pk>/",views.ProjectRemoveView.as_view(),name='wishlist-remove'),

    path("address/add/",views.AddressAddView.as_view(),name="details"),

    path("payment/verification/",views.PaymentVerification.as_view(),name="payment-verification"),

    path("my/orders/",views.MyOrdersView.as_view(),name="my-orders"),

    path('search/',views.SearchView.as_view(),name="search"),

    path("profile/<int:pk>/update",views.UserProfileUpdateView.as_view(),name="profile-update")


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
