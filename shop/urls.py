from django.contrib import admin
from django.urls import path, include
from .views import ProductListView, ProductDetailView, SignUp, CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ProductListView.as_view(), name="product_list"),
    path('category/<slug:category_slug>', ProductListView.as_view(), name="product_list_by_category"),
    path('product/<slug:slug>', ProductDetailView.as_view(), name="product_detail"),

    path('signup/', SignUp.as_view(), name = "signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)