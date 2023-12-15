from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauth.models import CustomUser
from django.utils.html import mark_safe
from django.db.models import F, ExpressionWrapper, DecimalField
from django.utils import timezone

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    


)

STATUS = (
    ('return_requested', 'Return Requested'),
    ('refund_requested', 'Refund Requested'),
    ('return_approved', 'Return Approved'),
    ('refund_approved', 'Refund Approved'),
    ('refund_successful', 'Refund Successful'),

)


RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

class TopCategory(models.Model):
    tcid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='tcat', alphabet="abcdefgh12345")
    title = models.CharField(max_length=200)
    


    class Meta:
        verbose_name_plural = "Top Categories"
    
    


    def __str__(self):
        return self.title




class MainCategory(models.Model):
    mcid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='mcat', alphabet="abcdefgh12345")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='main_category')
    top_category = models.ForeignKey(TopCategory, on_delete=models.SET_NULL, null=True, blank=True)



    class Meta:
        verbose_name_plural = "Main Categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


    def __str__(self):
        return self.title


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet="abcdefgh12345")
    top_category = models.ForeignKey(TopCategory, on_delete=models.SET_NULL, null=True, blank=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')
    class Meta:
        verbose_name_plural = "Categories"
    

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


    def __str__(self):
        return self.title
    

class Offer(models.Model):
    category = models.ForeignKey(TopCategory, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.category.title} - ${self.discount_amount} Off"



class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    user  = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    top_category = models.ForeignKey(TopCategory, on_delete=models.SET_NULL, null=True, blank=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True, blank=True, default='This is a Product')
    price = models.DecimalField(decimal_places=2, max_digits=999999999)
    old_price = models.DecimalField(decimal_places=2, max_digits=9999999999)
    type = models.CharField(max_length=150,null=True,blank=True)
    stock_count = models.IntegerField(null=True,blank=True)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"

    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    
    

class Size(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Product Size"

class Colour(models.Model):
    colour_code = models.CharField(max_length=50)
    
    def __str__(self):
        return self.colour_code

    class Meta:
        verbose_name_plural = "Product Colour"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=999999999)
    old_price = models.DecimalField(decimal_places=2, max_digits=9999999999)


    class Meta:
        verbose_name_plural = "Product Attributes"

    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images')
    product = models.ForeignKey(Product,related_name='p_image', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    
    class Meta:
        verbose_name_plural = "Product Images"



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_price = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    minimum_amount = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name_plural = "Coupon"









class CartOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='processing', null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=30, null=True, blank=True, default=None)
    # applied_coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    is_rejected = models.BooleanField(default=False, null=True, blank=True)






    class Meta:
        verbose_name_plural = "Cart Orders"


class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transactions = models.TextField(default='[]')  

    class Meta:
        verbose_name_plural = "Wallet"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200, null=True) 
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=99999999, decimal_places=2)
    total_price = models.DecimalField(max_digits=9999999999, decimal_places=2)


    class Meta:
        verbose_name_plural = "Cart Orders Items"

    


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))







class ProductReview(models.Model):
    user  = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural = "Products Review"


    def __str__(self):
        return self.product.title 
    

    def get_rating(self):
        return self.rating
    


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlist"


    def __str__(self):
        return self.product.title 
    

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=12, null=True)
    city = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    email = models.EmailField() 
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

    
