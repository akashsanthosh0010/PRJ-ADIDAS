from django.contrib import admin
from core.models import Product, Category, ProductImages, ProductReview, CartOrderItems, CartOrder, Address, Wishlist,MainCategory, TopCategory, Size, Colour, ProductAttribute, Coupon, Wallet, Offer

# Register your models here.


class ProductImageAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['user','title', 'product_image','price', 'old_price' ]

class ColourAdmin(admin.ModelAdmin):
    list_display = ['colour_code']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['title']

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product', 'colour', 'size', 'price', 'old_price',]

class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total_price']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_price', 'active']

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

class OfferAdmin(admin.ModelAdmin):
    list_display = ['category', 'discount_amount', 'start_date']

admin.site.register(Product, ProductAdmin)
admin.site.register(TopCategory, TopCategoryAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Colour, ColourAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Offer, OfferAdmin)








