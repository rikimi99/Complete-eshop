from django.urls import path, re_path, include
from . import views
from shop.views import *
from shop.forms import LoginForm
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('products/', ProductListView.as_view(), name='all_products'),
    path('products/', views.product_list, name='product_list'),  # Product list view
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('subcategory/<int:subcategory_id>/', ProductsBySubcategoryView.as_view(), name='products_by_subcategory'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('contactus/', views.contact, name='contactus'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('search/', views.search_results, name='search_results'),
    path('product-autocomplete/', product_autocomplete, name='product-autocomplete'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist-count/', wishlist_count_view, name='wishlist_count'),
    path('api/products/', get_products_json, name='api_products'),

]
