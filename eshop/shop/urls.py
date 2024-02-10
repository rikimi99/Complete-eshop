from django.urls import path, re_path, include
from . import views
from shop.views import CustomLoginView
from shop.forms import LoginForm
from shop.views import CustomLogoutView
from .views import checkout, product_autocomplete, order_success

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('products/', views.product_list, name='product_list'),  # Product list view
    path('cart/', views.cart, name='cart'), # Cart view
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart view
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove from cart view
    path('cart_count/', views.cart_count, name='cart_count'),  # Cart count view
    path('contactus/', views.contact, name='contactus'), # Contact us view
    path('checkout/', checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('search/', views.search_results, name='search_results'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product-autocomplete/', product_autocomplete, name='product-autocomplete'),
]