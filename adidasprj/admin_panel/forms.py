from django import forms
from django.forms import ModelForm
from userauth.models import CustomUser
from core.models import MainCategory, Category, Product, TopCategory, ProductImages, ProductAttribute, CartOrder, Coupon

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_blocked', 'f_name', 's_name', 'phone_no')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class TopCategoryForm(forms.ModelForm):

    class Meta:
        model = TopCategory
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super(TopCategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"




class MainCategoryForm(forms.ModelForm):

    class Meta:
        model = MainCategory
        fields = ['top_category','title', 'image']

    def __init__(self, *args, **kwargs):
        super(MainCategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


        
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['top_category','main_category','title', 'image',]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['user','top_category','main_category','category','title','old_price', 'price', 'image','description','in_stock','stock_count', 'type',]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImages
        fields = ['images',]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class ProductAttributeForm(forms.ModelForm):

    class Meta:
        model = ProductAttribute
        fields = ['product','price','old_price', 'colour', 'size']

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"          



class CartOrderForm(forms.ModelForm):

    class Meta:
        model = CartOrder
        fields = ['user','price','paid_status', 'product_status','status']

    def __init__(self, *args, **kwargs):
        super(CartOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['code','discount_price','active','valid_from', 'valid_to','minimum_amount', 'used',]

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"