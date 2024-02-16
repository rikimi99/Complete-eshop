from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.db.models.functions import Lower
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, CheckoutForm
from .models import *
from django.contrib.messages.views import SuccessMessageMixin

# View for the home page
def home(request):
    return render(request, 'shop/home.html')


# View for the user profile
@login_required
def profile(request):
    # Create or get the user's profile
    Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # If the request method is POST, process the update profile form
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            # If both forms are valid, save them and show success message
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        # If the request method is GET, show the profile update forms
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


# Class-based view for user registration
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect if user is already authenticated
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Render registration form
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Process registration form submission
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Custom LoginView with remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # Set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


# Custom LogoutView with success message and redirection
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        
        # Redirect to a specific page after logout
        self.next_page = reverse('where_to_redirect_after_logout') 
        return self.post(request, *args, **kwargs)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'  # Make sure this file extension is correct (it should be .txt, not mentioned in your snippet)
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


# View for listing products
def product_list(request):
    sort_by = request.GET.get('sort', 'name')
    products = Product.objects.all()
    if sort_by == 'price':
        products = products.order_by('price')
    else:
        products = products.order_by(Lower('name'))
    
    categories = Category.objects.prefetch_related('subcategories').all()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'stars_range': range(1, 6)  # Add this line
    })


# Class-based view for listing products
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'price':
            return Product.objects.all().order_by('price')
        else:
            return Product.objects.all().order_by(Lower('name'))

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)  # Ensure compatibility with Python 2 and 3
        context['categories'] = Category.objects.prefetch_related('subcategories').all()
        context['stars_range'] = range(1, 6)  # Add this line to include stars_range in the context
        return context


# Class-based view for listing products by category
class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('subcategories').all()
        return context


# Class-based view for listing products by subcategory
class ProductsBySubcategoryView(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        return Product.objects.filter(subcategory_id=subcategory_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('subcategories').all()
        return context


# View for getting products in JSON format
def get_products_json(request):
    products = Product.objects.all().values('id', 'name', 'price', 'description', 'image')
    products_list = list(products)
    return JsonResponse(products_list, safe=False)


# View for managing shopping cart
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    category_ids = set()

    for product_id, cart_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = int(cart_data.get('quantity', 0))
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        category_ids.add(product.category_id)
    recommended_products = Product.objects.filter(category__id__in=category_ids).exclude(id__in=cart.keys()).distinct()[:5]

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'recommended_products': recommended_products
    })


# View for adding a product to the cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if isinstance(cart[product_id_str], dict) and 'quantity' in cart[product_id_str]:
            cart[product_id_str]['quantity'] += 1
        else:
            cart[product_id_str] = {'quantity': 1}
    else:
        cart[product_id_str] = {'quantity': 1}
        
    request.session['cart'] = cart
    referer_url = request.META.get('HTTP_REFERER', reverse('home'))
    return HttpResponseRedirect(referer_url)


# View for removing a product from the cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1
        else:
            del cart[product_id_str] 
    request.session['cart'] = cart
    return HttpResponseRedirect(reverse('cart'))


# View for getting the count of items in the cart
def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.get(key, {}).get('quantity', 0) for key in cart.keys())
    return JsonResponse({'cart_count': cart_count})


# View for clearing the cart
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')


# View for the checkout process
def checkout(request):
    shipping_cost = 20
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, cart_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = int(cart_data.get('quantity', 0))
        subtotal = product.price * quantity
        total_price += subtotal
    total_price += shipping_cost
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session.pop('cart', None)
            return redirect('order_success')
    else:
        form = CheckoutForm()
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
    }
    return render(request, 'shop/checkout.html', context)


# View for showing order success page
def order_success(request):
    return render(request, 'shop/order_success.html')


# View for completing the order
def complete_order(request):
    if request.session.get('cart'):
        del request.session['cart']

    return redirect('order_success')


# View for searching products
def search_results(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'shop/search_results.html', {'products': products})


# View for product autocomplete API
def product_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET['term']
        products = Product.objects.filter(name__istartswith=term)[:10]
        data = [{'name': product.name, 'image_url': product.image.url, 'price': product.price} for product in products]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


# View for getting similar products
def get_similar_products(product_id):
    product = get_object_or_404(Product, id=product_id)
    category = product.category
    similar_products = Product.objects.filter(category=category).exclude(id=product_id)[:5]
    return similar_products


# View for submitting a rating for a product
def rate_product(request, product_id):
    if request.method == 'POST':
        stars = request.POST.get('stars', 0)
        try:
            stars = int(stars)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating value'}, status=400)

        if stars < 1 or stars > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)

        product = get_object_or_404(Product, id=product_id)
        rating, created = Rating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'stars': stars}
        )

        return JsonResponse({'success': 'Rating updated', 'rating': stars, 'created': created})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# View for the contact us page
def contact(request):
    return render(request, 'shop/contactus.html')


# View for the wishlist page
def wishlist_view(request):
    if request.user.is_authenticated:
        # Fetch wishlist items for the logged-in user
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
        context = {'wishlist_items': wishlist_items}
    else:
        # If the user is not authenticated, redirect to login or show an empty page
        context = {'wishlist_items': []}  # Adjust as necessary
    return render(request, 'shop/wishlist.html', context)


# View for getting the count of items in the wishlist
def wishlist_count_view(request):
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return JsonResponse({'wishlist_count': count})
