from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views

# Define URL patterns for the shop application
urlpatterns = [
    # Home page - Displays the main landing page of the shop
    path('', views.home, name='home'),

    # User registration - Allows new users to register
    path('register/', views.RegisterView.as_view(), name='register'),

    # User login - Handles user login with custom functionality
    path('login/', views.CustomLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='users/login.html',
        authentication_form=views.LoginForm
    ), name='login'),

    # User logout - Logs out users and redirects as necessary
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # User profile - Allows users to view and edit their profile
    path('profile/', views.profile, name='profile'),

    # OAuth URLs - For social authentication with external services
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

    # Password reset - Sends a password reset email to users
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),

    # Password reset confirmation - Allows users to enter a new password
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # Password reset complete - Informs users that their password has been reset
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    # Password change - Allows users to change their password
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),

    # Product listing - Lists all products
    path('products/', views.product_list, name='product_list'),

    # Products by category - Filters products by their category
    path('category/<int:category_id>/', views.ProductsByCategoryView.as_view(), name='products_by_category'),

    # Products by subcategory - Filters products by their subcategory
    path('subcategory/<int:subcategory_id>/', views.ProductsBySubcategoryView.as_view(), name='products_by_subcategory'),

    # Shopping cart - Displays the user's shopping cart
    path('cart/', views.cart, name='cart'),

    # Add product to cart - Adds a specific product to the shopping cart
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove product from cart - Removes a specific product from the shopping cart
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Cart count - Returns the number of items in the shopping cart
    path('cart_count/', views.cart_count, name='cart_count'),

    # Contact us page - Displays the contact information
    path('contactus/', views.contact, name='contactus'),

    # Checkout process - Handles the checkout process
    path('checkout/', views.checkout, name='checkout'),

    # Order success page - Displays a message upon successful order completion
    path('order_success/', views.order_success, name='order_success'),

    # Complete order - Finalizes the order process
    path('complete_order/', views.complete_order, name='complete_order'),

    # Search results page - Shows the results of a product search
    path('search/', views.search_results, name='search_results'),

    # Product autocomplete API - Provides product suggestions as the user types
    path('product-autocomplete/', views.product_autocomplete, name='product-autocomplete'),

    # Products API - Returns a list of products in JSON format
    path('api/products/', views.get_products_json, name='api_products'),

]