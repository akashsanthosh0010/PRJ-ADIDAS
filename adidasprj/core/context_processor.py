from .models import TopCategory, Category, Product
from django.db.models import Min, Max

def default(request):
    top = TopCategory.objects.all()
    cat = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))
    return { 
        'top':top,
        'cat': cat,
        'min_max_price': min_max_price
    }
    