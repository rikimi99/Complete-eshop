from django.urls import path, re_path, include
from . import views

# Define URL patterns for the shop application
urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # User registration
    path('register/', views.RegisterView.as_view(), name='register'),

    # User login
    path('login/', views.CustomLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='users/login.html',
        authentication_form=views.LoginForm
    ), name='login'),

    # User logout
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # User profile
    path('profile/', views.profile, name='profile'),

    # OAuth URLs
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

    # Product listing
    path('products/', views.product_list, name='product_list'),

    # Products by category
    path('category/<int:category_id>/', views.ProductsByCategoryView.as_view(), name='products_by_category'),

    # Products by subcategory
    path('subcategory/<int:subcategory_id>/', views.ProductsBySubcategoryView.as_view(), name='products_by_subcategory'),

    # Shopping cart
    path('cart/', views.cart, name='cart'),

    # Add product to cart
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove product from cart
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Cart count
    path('cart_count/', views.cart_count, name='cart_count'),

    # Contact us page
    path('contactus/', views.contact, name='contactus'),

    # Checkout process
    path('checkout/', views.checkout, name='checkout'),

    # Order success page
    path('order_success/', views.order_success, name='order_success'),

    # Complete order
    path('complete_order/', views.complete_order, name='complete_order'),

    # Search results page
    path('search/', views.search_results, name='search_results'),

    # Product autocomplete API
    path('product-autocomplete/', views.product_autocomplete, name='product-autocomplete'),

    # Wishlist view
    path('wishlist/', views.wishlist_view, name='wishlist'),

    # Wishlist count
    path('wishlist-count/', views.wishlist_count_view, name='wishlist_count'),

    # Products API
    path('api/products/', views.get_products_json, name='api_products'),
]
