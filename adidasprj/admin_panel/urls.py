from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('admin_coupons/',views.admin_coupons,name='admin_coupons'),
    path('admin_orderes/',views.admin_orders,name='admin_orders'),
    path('admin_cart/',views.admin_cart,name='admin_cart'),
    path('admin_categories/',views.admin_categories,name='admin_categories'),
    path('admin_main_categories/',views.admin_main_categories,name='admin_main_categories'),
    path('admin_products/',views.admin_products,name='admin_products'),
    path('admin_products_review/',views.admin_product_review,name='admin_products_review'),
    path('admin_wishlist/',views.admin_wishlist,name='admin_wishlist'),
    path('admin_users/',views.admin_users,name='admin_users'),
    path('admin_user_edit/<id>',views.user_edit,name='admin_user_edit'),
    path('admin_add_user/',views.add_user,name='admin_add_user'),
    path('admin_user_delete/<id>',views.delete_user,name='admin_user_delete'),
    path('add_main_category/',views.add_main_category,name='add_main_category'),
    path('delete_main_category/<id>',views.delete_main_category,name='delete_main_category'),
    path('delete_category/<id>',views.delete_category,name='delete_category'),
    path('edit_category/<id>',views.edit_category,name='edit_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('add_product/',views.add_product,name='add_product'),
    path('add_product_images/',views.add_product_images,name='add_product_images'),
    path('edit_product/<id>',views.edit_product,name='edit_product'),                              
    path('delete_product/<id>',views.delete_product,name='delete_product'), 
    path('edit_main_category/<id>',views.edit_main_category,name='edit_main_category'),
    path('delete_top_category/<id>',views.delete_top_category,name='delete_top_category'),
    path('edit_top_category/<id>',views.edit_top_category,name='edit_top_category'),
    path('add_top_category/',views.add_top_category,name='add_top_category'),
    path('admin_top_categories/',views.admin_top_categories,name='admin_top_categories'),
    path('admin_products_attributes/',views.admin_products_attributes,name='admin_products_attributes'),
    path('add_product_attributes/',views.add_product_attributes,name='add_product_attributes'),
    path('edit_product_attributes/<id>',views.edit_product_attributes,name='edit_product_attributes'),
    path('delete_product_attributes/<id>',views.delete_product_attributes,name='delete_product_attributes'),
    path('edit_order/<id>',views.edit_order,name='edit_order'),                              
    path('delete_order/<id>',views.delete_order,name='delete_order'), 
    path('add_coupons/',views.add_coupon,name='add_coupons'),
    path('edit_coupons/<id>',views.edit_coupon,name='edit_coupons'),                              
    path('delete_coupons/<id>',views.delete_coupon,name='delete_coupons'), 
    path('view_order_product/<id>',views.view_order_product,name='view_order_product'),
    path('sales_report/',views.sales_report,name='sales_report'),
    path('sales_report_csv/',views.sales_report_csv, name='sales_report_csv'),
    path('sales_report_pdf/',views.sales_report_pdf, name='sales_report_pdf'),

    





    




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)