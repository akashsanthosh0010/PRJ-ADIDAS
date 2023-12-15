from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('base/',views.base,name='base'),
    path('', views.home_view,name='home'),
    path('auto_complete', views.auto_complete,name='auto_complete'),
    path('register/',views.register_user,name='register'),
    path('request_otp/',views.request_otp,name='request_otp'),
    path('resend_otp/',views.resend_otp, name='resend_otp'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('login/',views.login_user,name='login'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_sent/', views.password_reset_sent_view, name='password_reset_sent'),
    path('save_new-password/', views.save_new_password, name='save_new_password'),
    path('logout/',views.log_out,name='logout'),
    path('view_product/<pid>',views.view_product,name='view_product'),
    path('mens_categories_product/<str:title>',views.top_categories_product,name='mens_categories_product'),
    path('main_categories_product/<str:title>',views.main_categories_product,name='main_categories_product'),
    path('categories_product/<str:title>',views.categories_product,name='categories_product'),
    path('search/',views.search_view,name='search'),
    path('filter-products/', views.filter_product, name='filter-product'),
    path('product_cart/',views.product_cart,name='add-to-cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
    path('delete-from-cart/',views.delete_item_from_cart,name='delete-from-cart'),
    path('update-cart/',views.update_cart,name='update-cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_completed/', views.payment_completed_view, name = 'payment_completed'),
    path('invoice_pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('payment_failed/', views.payment_failed_view, name = 'payment_failed'),
    path('wallet/', views.view_wallet, name='wallet'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_address/', views.user_address, name='user_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('make_default_address/', views.make_address_default, name='make_default_address'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:id>', views.order_detail, name='order_detail'),
    path('user_invoice/<int:id>', views.user_invoice, name='user_invoice'),
    path('cancel_order/<int:order_id>/',views.cancel_order, name='cancel_order'),
    path('delete_order_product/<int:product_id>/',views.delete_order_product, name='delete_order_product'),
    path('refund_order/<int:order_id>/', views.refund_order, name='refund_order'),
    path('approve_refund/<int:order_id>/', views.approve_refund, name='approve_refund'),
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('test/', views.test, name='test'),













    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)