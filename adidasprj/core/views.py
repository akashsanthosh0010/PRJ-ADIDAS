from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages  
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from userauth.models import CustomUser 
from django.contrib.auth import authenticate, login
from .utils import generate_otp,send_otp_email,check_otp, generate_referral_code
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.template.loader import render_to_string, get_template
from core.models import Product, Category, ProductImages,Coupon, ProductReview, CartOrderItems, CartOrder, Address, Wishlist,MainCategory,TopCategory, Wallet
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from email.message import EmailMessage
import smtplib
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.db.models import Count
from xhtml2pdf import pisa
from decimal import Decimal



# Create your views here.
def base(request):
    top = TopCategory.objects.all()
    context = {'top': top}
    return render(request, 'base.html', context)


def home_view(request):
    if request.user.is_authenticated:
        # User is authenticated using any method (Google, username/password, etc.)
        products = Product.objects.all()
        top = TopCategory.objects.all()
        context = {
            'products': products,
            'top': top
        }
        return render(request, 'home.html', context)

    # Check if the user has authenticated via Google
    if 'username' in request.session:
        # User has a session variable, consider additional checks if needed
        products = Product.objects.all()
        top = TopCategory.objects.all()
        context = {
            'products': products,
            'top': top
        }
        return render(request, 'home.html', context)

    # If not authenticated or not authenticated via Google, redirect to login
    return redirect('login')


def auto_complete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)
    return render(request, 'base.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        referral_code = request.POST.get('referral_code')

        try:
            # Attempt to create a new user
            my_user = CustomUser.objects.create_user(username, email, password)
            my_user.save()
            Wallet.objects.create(user=my_user)

            my_user.referral_code = generate_referral_code()
            my_user.referral_code_used = False
            my_user.save()
            

        except IntegrityError:
            # IntegrityError occurs when a user with the provided email already exists
            messages.warning(request, f"A user with {username} already exists.")
            return redirect('register')

        # Referral code checking (moved outside the except block)
        user = authenticate(username=username, password=password)
        if referral_code:
            try:
                referred_user = CustomUser.objects.get(referral_code=referral_code)
                if not referred_user.referral_code_used:
                    referred_user.wallet.balance += 100
                    referred_user.wallet.save()
                    referred_user.referral_code_used = True
                    referred_user.save()
                    user.wallet.balance += 100
                    user.wallet.save()
                    user.save()
                    messages.success(request, "Referral code successfully applied!")
                else:
                    messages.error(request, "Referral code is already used.")
                    return redirect('register')
            except CustomUser.DoesNotExist:
                messages.error(request, "Referral code does not exist.")
                return redirect('register')
            
        return redirect('request_otp')    
    return render(request, 'register.html')

# views.py

def request_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        generated_otp = request.session.get('generated_otp')

        if generated_otp:
            # Resend OTP
            send_otp_email(email, generated_otp)
            return redirect('verify_otp')
        else:
            # New OTP generation and sending
            otp = generate_otp()
            send_otp_email(email, otp)
            request.session['generated_otp'] = otp
            request.session['email'] = email
            return redirect('verify_otp')

    return render(request, 'request_otp.html')


# views.py

def resend_otp(request):
    if 'email' in request.session:
        email = request.session['email']
        otp = generate_otp()
        send_otp_email(email, otp)
        request.session['generated_otp'] = otp
        return redirect('verify_otp')
    else:
        # Handle the case when there is no email in the session
        return HttpResponse("Email not found in session.")


def verify_otp(request):
    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp')
        email = request.session.get('email')

        if check_otp(submitted_otp, generated_otp):
            return redirect(login_user)
        
        messages.error(request, "Invalid OTP")
        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

from django.contrib import messages

def login_user(request):
    if 'username' in request.session:
        return redirect(home_view)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active and not user.is_blocked:
            login(request, user)
            request.session['username'] = username
            return redirect(home_view)
        elif user is not None and user.is_blocked:
            messages.error(request, "Your account is blocked. Please contact support.")
        else:
            messages.error(request, "Your username and password didn't match.")
    return render(request, 'login.html')



User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username=username).first()  # Use CustomUser

        if user:
            # Generate a unique token for password reset
            token = default_token_generator.make_token(user)

            # Save the token in the database (you may want to create a model for this)
            user.password_reset_token = token
            user.save()

            # Send the reset password email
            reset_password_url = f"{settings.BASE_URL}/reset_password/?token={token}"
            subject = 'Your Password Reset link'
            message = f'Your Password Reset link : {reset_password_url}'
            from_email = 'akashsanthosh0010@gmail.com'  # Replace with your email
            recipient_list = [user.email]

            msg = EmailMessage()
            msg['From'] = from_email
            msg['To'] = user.email  # Change this line to use a string, not a list
            msg['Subject'] = subject
            msg.set_content(message)

            with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
                server.starttls()
                server.login("307ed7b20b1e45", "9c12fc68c768a4")
                server.send_message(msg)

            return redirect('password_reset_sent')

    return render(request, 'forgot_password.html')

def password_reset_sent_view(request):
    return render(request, 'password_reset_sent.html')

def reset_password(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        user = CustomUser.objects.filter(password_reset_token=token).first()

        if user and default_token_generator.check_token(user, token):
            # Token is valid, render the reset password form
            return render(request, 'reset_password_form.html', {'token': token})

    # Token is invalid or not provided
    messages.error(request, 'Invalid or expired password reset link.')
    return redirect('login')  # Redirect to login or another appropriate page

def save_new_password(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = CustomUser.objects.filter(password_reset_token=token).first()

        if user and default_token_generator.check_token(user, token):
            # Token is valid, update the user's password
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.password_reset_token = None  # Clear the reset token
            user.save()

            messages.success(request, 'Your password has been successfully reset. You can now log in with your new password.')
            return redirect('login')  # Redirect to login or another appropriate page

    # Token is invalid or not provided
    messages.error(request, 'Invalid or expired password reset link.')
    return redirect('login')  # Redirect to login or another appropriate page



def log_out(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect(login_user)


def view_product(request, pid):
    try:
        product = Product.objects.get(pid=pid)
        products = Product.objects.filter(category = product.category)
        product_images = product.p_image.all()
        context = {'product' : product, 'product_images':product_images, 'products':products}
        return render(request,'product_detail.html', context)
    except Product.DoesNotExist:
        return render(request, '404error.html')


def top_categories_product(request, title ):
    mens_categories = MainCategory.objects.filter(top_category__title = title)
    context = {'mens_category':mens_categories}
    return render(request,'mens_categories_product.html', context)


def main_categories_product(request, title ):
    mens_categories = Category.objects.filter(main_category__title = title)
    context = {'mens_category':mens_categories}
    return render(request,'main_cat_product.html', context)


def categories_product(request, title ):
    mens_categories = Product.objects.filter(category__title = title)
    context = {'mens_category':mens_categories}
    return render(request,'cat_product.html', context)



def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']


    products = Product.objects.all().distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    context = {
        'products': products,

    }

    data = render_to_string('search-filter.html', context )
    return JsonResponse({'data': data})


def product_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
        'stock_count' : request.GET['stock_count'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product


    return JsonResponse({'data':request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj'])})
    


def cart_view(request):
    cart_total_amount = 0
    coupon_discount = 0

    # Check if a coupon is applied
    if 'applied_coupon' in request.session:
        coupon_code = request.session['applied_coupon']
        try:
            coupon = Coupon.objects.get(
                code=coupon_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            coupon_discount = coupon.discount_price
        except Coupon.DoesNotExist:
            # Handle the case where the stored coupon is no longer valid
            pass


    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        cart_total_amount_discount = cart_total_amount
        cart_total_amount_discount -= coupon_discount
        request.session['cart_total_amount'] = cart_total_amount

        return render(request,'product_cart.html', {'cart_data':request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'coupon_discount': coupon_discount,'cart_total_amount_discount' : cart_total_amount_discount})
    else:
        return redirect (home_view)
    


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code,
                    active=True,
                    valid_from__lte=timezone.now(),
                    valid_to__gte=timezone.now(),
                    used = False
                )


                cart_total_amount = request.session.get('cart_total_amount', 0)

                # Check if the total cart amount is greater than the minimum amount required by the coupon
                if cart_total_amount >= coupon.minimum_amount:
                    # Store applied coupon in the session
                    request.session['applied_coupon'] = coupon.code

                    messages.success(request, 'Coupon applied successfully!')
                else:
                    messages.error(request, 'Total cart amount must be greater than the minimum amount required by the coupon.')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code or coupon has expired.')
        else:
            messages.error(request, 'Coupon code is required.')

    return redirect(cart_view)

def remove_coupon(request):
    # Implement the ability to remove the applied coupon
    if 'applied_coupon' in request.session:
        del request.session['applied_coupon']
        messages.success(request, 'Coupon removed successfully!')

    return redirect(cart_view)

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('cart_list.html', {'cart_data':request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems':len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('cart_list.html', {'cart_data':request.session['cart_data_obj'], 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({'data': context, 'totalcartitems':len(request.session['cart_data_obj'])})



def user_address(request):
    user = request.user
    try:
        user_details = Address.objects.filter(user=user)
    except Address.DoesNotExist:
        user_details = None

    if request.method == "POST":
        # Update basic profile information
        name = request.POST.get('name')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        city = request.POST.get('city')


            # Create a new address
        new_address = Address.objects.create(
                user=user,
                name=name,
                address=address,
                phone_no=phone_no,
                city=city,
                landmark=landmark,
                email=email,
            )
        messages.success(request, 'Address Added Successfully.')

        return redirect(user_address)
    context = {'user_details' : user_details}

    return render(request, 'user_address.html', context)


def delete_address(request, id):
    address = Address.objects.get(id=id, user=request.user)
    address.delete()
    return redirect(user_address)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean': True})



def checkout_view(request):

    applied_coupon_code = request.session.get('applied_coupon')
    # Check if the applied coupon code is valid and not used
    if applied_coupon_code:
        try:
            coupon = Coupon.objects.get(
                code=applied_coupon_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now(),
                used=False
            )

            # Mark the coupon as used
            coupon.used = True
            coupon.save()

            # Set applied_coupon in session to True
            request.session['applied_coupon'] = True
        except Coupon.DoesNotExist:
            # Handle the case where the coupon is not found or is invalid
            pass



    cart_total_amount = request.session.get('cart_total_amount', 0)

    try:
        active_address = Address.objects.get(user=request.user, status=True)

        # If the user's address exists, proceed to create the order
        total_amount = 0
        out_of_stock_products = []

        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                product = Product.objects.get(id=p_id)
                if product.stock_count <= 0:
                    out_of_stock_products.append(product.title)
                else:
                    total_amount += int(item['qty']) * float(item['price'])
                    product.stock_count -= int(item['qty'])
                    product.save()

            if out_of_stock_products:
                messages.warning(
                    request,
                    f"The following products are out of stock: {', '.join(out_of_stock_products)}"
                )
                return redirect(cart_view)        
            order = CartOrder.objects.create(
                user=request.user,
                price=int(cart_total_amount)
            )
            request.session['order_id'] = order.id
            for p_id, item in request.session['cart_data_obj'].items():

                cart_order_product = CartOrderItems.objects.create(
                    order=order,
                    product=product,
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total_price=float(item['qty']) * float(item['price'])
                )


        host = request.get_host()
        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(cart_total_amount),
            'item_name': 'Order-Item-No-3',
            'Invoice': 'INV_NO-4',
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_completed')),
            'cancel_url': 'http://{}{}'.format(host, reverse('payment_failed')),


        }

        paypal_payment_button = PayPalPaymentsForm(initial = paypal_dict)

        context = {
            'active_address': active_address,
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'paypal_payment_button': paypal_payment_button
        }


        return render(request, 'checkout.html', context)

    except Address.DoesNotExist:
        # Handle the case where the user's address does not exist
        active_address = None
        messages.warning(
            request,
            'Please add your address before proceeding to checkout.'
        )
        return redirect(cart_view)


def cash_on_delivery(request):
    request.session.pop('cart_data_obj', None)
    return render(request, 'cash_on_delivery.html')


def payment_completed_view(request):
    
    if 'cart_data_obj' in request.session:
        cart_total_amount = request.session.get('cart_total_amount', 0)

    applied_coupon_code = request.session.get('applied_coupon')

    # Initialize applied_discount_amount to 0 (default value)
    applied_discount_amount = 0

    # If an applied coupon code is present, fetch the corresponding coupon
    if applied_coupon_code:
        try:
            # Assuming 'discount_price' is the field representing the discount amount in your Coupon model
            applied_coupon = Coupon.objects.get(
                code=applied_coupon_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            applied_discount_amount = applied_coupon.discount_price
        except Coupon.DoesNotExist:
            # Handle the case where the coupon is not found or is invalid
            pass

    order_id = request.session.get('order_id')
    order = CartOrder.objects.get(id=order_id, user=request.user)
    order.paid_status = True
    order.save()

    context = {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'applied_discount_amount' : applied_discount_amount,
        
    }

    # request.session.pop('cart_data_obj', None)

    return render(request, 'payment_completed.html', context)


def invoice_pdf(request):
    if 'cart_data_obj' in request.session:
        cart_total_amount = request.session.get('cart_total_amount', 0)

    applied_coupon_code = request.session.get('applied_coupon')

    # Initialize applied_discount_amount to 0 (default value)
    applied_discount_amount = 0

    # If an applied coupon code is present, fetch the corresponding coupon
    if applied_coupon_code:
        try:
            # Assuming 'discount_price' is the field representing the discount amount in your Coupon model
            applied_coupon = Coupon.objects.get(
                code=applied_coupon_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            applied_discount_amount = applied_coupon.discount_price
        except Coupon.DoesNotExist:
            # Handle the case where the coupon is not found or is invalid
            pass

    template_path = 'pdf_report.html'
    context = {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'applied_discount_amount' : applied_discount_amount,
        
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'


    pdf_context = {'page-width': '10in', 'page-height': '10in'}
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
    request.session.pop('cart_data_obj', None)
    

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def payment_failed_view(request):
    return render(request, 'payment_failed.html')

def view_wallet(request):
    user_wallet = request.user.wallet
    context = {'wallet': user_wallet}
    return render(request, 'wallet.html', context)

def user_profile(request):
    user = request.user

    if request.method == "POST":
        # Update basic profile information
        f_name = request.POST.get('f_name')
        s_name = request.POST.get('s_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')

        if f_name:
            user.f_name = f_name
        if s_name:
            user.s_name = s_name
        if email:
            user.email = email
        if phone_no:
            user.phone_no = phone_no

        user.save()
    context = {'user': user}
    return render(request, 'user_profile.html', context)


def change_password(request):
    user = request.user
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if password and new_password and confirm_password:
    # Check if the entered current password is correct
        if user.check_password(password):
            # Check if the new password and confirm password match
            if new_password == confirm_password:
                # Set the new password using set_password
                user.set_password(new_password)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')
    return render(request, 'change_password.html')




def order_list(request):
    orders = CartOrder.objects.filter(user=request.user)
    context = {
        'orders' : orders,
            }
    return render(request, 'order_list.html', context)




def refund_order(request, order_id):
    # Check if the order is already refunded or in a state where a refund can be initiated
    order = CartOrder.objects.get(id=order_id, user=request.user)

    if order.status == 'refund_approved':
        messages.warning(request, 'This order has already been refunded.')
        return redirect(order_list)  # Update with your actual redirect URL


    # Check if the order has been paid
    if not order.paid_status:
        messages.error(request, 'Refund can only be initiated for paid orders.')
        return redirect(order_list)  # Update with your actual redirect URL

    # Update order status to 'refund_requested' or another appropriate status
    order.status = 'refund_requested'
    order.save()

    # You might want to redirect the user or render a confirmation template
    messages.success(request, 'Refund request initiated successfully. Amount refunded to the wallet.')
    return redirect(order_list)  # Update with your actual success URL



def approve_refund(request, order_id):
    # Get the order
    order = CartOrder.objects.get(id=order_id, user=request.user)

    cart_total_amount = request.session.get('cart_total_amount', 0)

    
    # Check if the order is already refunded
    if order.status == 'refund_approved':
        
        try:
            # Update the wallet balance
            # user = request.user
            wallet = Wallet.objects.get(user=order.user)
            wallet_balance_before = wallet.balance 
            cart_total_amount_decimal = Decimal(cart_total_amount)
            formatted_cart_total = "{:.2f}".format(cart_total_amount_decimal)
            wallet.balance += Decimal(formatted_cart_total)
            wallet.save()
            order.status = 'refund_successful'
            order.save()


            # No need to update the order status here, assuming it's already done by the admin

            messages.success(request, 'Refund approved successfully. Amount refunded to the wallet.')
            return redirect(order_list)  # Update with your actual redirect URL

        except Exception as e:
            # Handle any errors that may occur during the refund process
            messages.error(request, f'Error approving refund: {str(e)}')
            return redirect(reverse('order_list'))







def cancel_order(request, order_id):
    if request.method == 'POST':
        order = CartOrder.objects.get(id = order_id)
        order.delete()
        return redirect(order_list)

    return redirect(order_list)


def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {'products': products}
    return render(request,'order_detail.html', context)


def user_invoice(request, id):
    orders = CartOrder.objects.filter(user=request.user)
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {
        'products': products,
        'order': order
    }
    return render(request, 'user_invoice.html', context)

def delete_order_product(request, product_id):
    if request.method == 'POST':
        product = CartOrderItems.objects.get(id = product_id)
        order_id = product.order.id
        order = CartOrder.objects.get(id=order_id)
        order.price -= product.total_price
        order.save()
        product.delete()
        return redirect(order_detail, id=order_id)
    return redirect(order_detail)






def test(request):
    categories_with_counts = Category.objects.annotate(product_count=Count('product'))

    # Prepare data for the graph
    data_for_graph = [{'name': category.title, 'count': category.product_count} for category in categories_with_counts]

    # Pass the data to the template
    context = {
        'data_for_graph': data_for_graph,}
    return render(request, 'test.html', context)




