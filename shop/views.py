from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Category, Product
from django.views.generic import ListView, DetailView, FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('product_list')

class CustomLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    success_url = reverse_lazy('product_list')
    
class SignUp(FormView):
    template_name = "accounts/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        categoty_slug = self.kwargs.get("category_slug")
        if categoty_slug:
            category = get_object_or_404(Category, slug = categoty_slug)
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = None
        if 'category_slug' in self.kwargs:
            context["category"] = get_object_or_404(Category, slug = self.kwargs['category_slug'])
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product/product_detail.html"
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs['slug'])