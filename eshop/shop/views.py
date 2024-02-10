from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models.functions import Lower
from .models import *

def home(request):
    return render(request, 'shop/home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='#')

        return render(request, self.template_name, {'form': form})
    
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        
        self.next_page = reverse('where_to_redirect_after_logout') 
        return self.post(request, *args, **kwargs)








    
def product_list(request):
    sort_by = request.GET.get('sort', 'name')
    products = Product.objects.all()
    if sort_by == 'price':
        products = products.order_by('price')
    else:
        products = products.order_by(Lower('name'))
    return render(request, 'shop/product_list.html', {'products': products})

def contact(request):
    return render(request, 'shop/contactus.html')

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

def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.get(key, {}).get('quantity', 0) for key in cart.keys())
    return JsonResponse({'cart_count': cart_count})

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')

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

def order_success(request):
    return render(request, 'shop/order_success.html')

def complete_order(request):
    if request.session.get('cart'):
        del request.session['cart']

    return redirect('order_success')

def search_results(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'shop/search_results.html', {'products': products})

def product_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET['term']
        products = Product.objects.filter(name__istartswith=term)[:10]
        data = [{'name': product.name, 'image_url': product.image.url, 'price': product.price} for product in products]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def get_similar_products(product_id):
    product = get_object_or_404(Product, id=product_id)
    category = product.category
    similar_products = Product.objects.filter(category=category).exclude(id=product_id)[:5]
    return similar_products

def submit_rating(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Rating.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_ratings_comments(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=product_id)
        ratings_comments = Rating.objects.filter(product=product).order_by('-created_at')
        data = [{'user': rc.user.username if rc.user else 'Anonymous',
                 'rating': rc.rating,
                 'comment': rc.comment,
                 'created_at': rc.created_at.strftime('%Y-%m-%d %H:%M:%S')} for rc in ratings_comments]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_rating(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        rating_value = request.POST.get('rating')
        comment = request.POST.get('comment')
        rating, created = Rating.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating_value, 'comment': comment}
        )
        return JsonResponse({'success': True, 'created': created})
    return JsonResponse({'success': False})