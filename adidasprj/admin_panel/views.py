from django.shortcuts import render, redirect
from .forms import UserForm, MainCategoryForm, CategoryForm, ProductForm, TopCategoryForm, ProductImageForm, ProductAttributeForm, CartOrderForm, CouponForm
from userauth.models import CustomUser
from django.contrib import messages
from core.models import MainCategory, Category, Product, TopCategory, ProductImages, ProductAttribute, CartOrder, Coupon, CartOrderItems
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse, FileResponse
import csv
from django.utils.encoding import smart_str
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.

def admin_panel(request):
    filter_type = request.GET.get('filter', 'month')  # Default to 'month' if no filter is provided

    if filter_type == 'month':
        products_by_order_date = CartOrderItems.objects.select_related('product', 'order')\
            .annotate(order_date=TruncMonth('order__order_date'))\
            .values('order_date')\
            .annotate(product_count=Count('product'))
    elif filter_type == 'year':
        products_by_order_date = CartOrderItems.objects.select_related('product', 'order')\
            .annotate(order_date=TruncYear('order__order_date'))\
            .values('order_date')\
            .annotate(product_count=Count('product'))

    cart_order_items = CartOrderItems.objects.select_related('product','order').all()




    # Prepare data for the graph
    data_for_graph = [{'date': entry['order_date'], 'count': entry['product_count']} for entry in products_by_order_date]
    total_revenue = CartOrder.objects.aggregate(Sum('price'))['price__sum'] or 0
    total_orders = CartOrder.objects.count()
    total_users = CustomUser.objects.count()
    # Pass the data to the template
    context = {
        'data_for_graph': data_for_graph,
        'total_revenue' : total_revenue,
        'total_orders': total_orders,
        'total_users' : total_users,
        'cart_order_items' : cart_order_items
        }
    return render(request, 'index.html', context)


def sales_report(request):
    

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        # Perform filtering based on the date range
        cart_order = CartOrderItems.objects.filter(order__order_date__range=[from_date, to_date])
    else:
        # Default behavior without filtering
        cart_order = CartOrderItems.objects.select_related('product','order').all()

    context = {
        'cart_order': cart_order,
    }
    return render(request, 'sales_report.html', context)


def sales_report_csv(request):
    
    # Perform filtering based on the date range
    cart_order = CartOrderItems.objects.select_related('product','order').all()

    # Create a response with the correct content type for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sales_report.csv'

    # Create a CSV writer
    csv_writer = csv.writer(response)
    
    # Write headers to the CSV file
    csv_writer.writerow(['Product', 'Product ID','Quantity', 'Amount','Total Amount','Is_Paid', 'Shipping'])

    # Write data to the CSV file
    for order in cart_order:
        csv_writer.writerow([
            smart_str(order.product.title),
            smart_str(order.product.pid),
            smart_str(order.qty),
            smart_str(order.product.price),
            smart_str(order.order.price),
            smart_str(order.order.paid_status),
            smart_str(order.order.product_status)
        ])

    return response


# def sales_report_pdf(request):
#     buf = io.BytesIO()
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     textob = c.beginText()
#     textob.setTextOrigin(inch, inch)
#     textob.setFont('Helvetica', 14)

#     lines = []

#     cart_order = CartOrderItems.objects.select_related('product','order').all()

#     for order in cart_order:
#         lines.append(order.product.title)
#         lines.append(order.product.pid)
#         lines.append(str(order.product.price))
#         lines.append(order.order.product_status)
#         lines.append('')


#     for line in lines:
#         textob.textLine(line)

#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)


#     return FileResponse(buf, as_attachment=True, filename='sales-report.pdf')


def sales_report_pdf(request):
    buf = io.BytesIO()
    pdf = SimpleDocTemplate(buf, pagesize=letter)

    # Create a list to hold the data for the table
    table_data = [
        ['Title', 'Product ID', 'Quantity','Amount','Total Amount', 'Is_Paid', 'Status'],
    ]

    cart_order = CartOrderItems.objects.select_related('product', 'order').all()

    for order in cart_order:
        table_data.append([
            order.product.title,
            order.product.pid,
            str(order.qty),
            str(order.product.price),
            str(order.order.price),
            order.order.paid_status,
            order.order.product_status,
        ])

    # Create the main table and set its style
    table = Table(table_data, colWidths='*')
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, 0), 1, colors.white),
        ('GRID', (0, -1), (-1, -1), 1, colors.white),
    ])

    table.setStyle(style)

    # Create a title with a different style
    title_text = '<b>Sales Report</b>'
    title_style = getSampleStyleSheet()['Title']
    title = Paragraph(title_text, title_style)

    # Build the PDF
    elements = [title,Spacer(1, 30), table]  # Switched the order
    pdf.build(elements)

    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='sales-report.pdf')



def admin_coupons(request):
    form = Coupon.objects.all()
    context = {'form':form}
    return render(request, 'coupons.html', context)

def admin_orders(request):
    form = CartOrder.objects.all()
    context = {'form':form}
    return render(request, 'orders.html', context)

def admin_cart(request):
    
    return render(request, 'cart.html')

def admin_categories(request):
    form = Category.objects.all()
    context = {'form': form}
    return render(request, 'categories.html', context)

def admin_main_categories(request):
    form = MainCategory.objects.all()
    context = {'form': form}
    return render(request, 'main_categories.html', context)

def admin_top_categories(request):
    form = TopCategory.objects.all()
    context = {'form': form}
    return render(request, 'top_category.html', context)

def admin_products(request):
    form = Product.objects.all()
    context = {'form':form}
    return render(request, 'products.html', context)

def admin_product_review(request):
    return render(request, 'product_review.html')

def admin_wishlist(request):
    return render(request, 'wishlist.html')

def admin_users(request):
    data = CustomUser.objects.all()
    context = {'data':data}
    
    return render(request, 'user.html', context)

def user_edit(request,id):
    user = CustomUser.objects.get(id=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect(admin_users)
    context = {'form':form}
    return render(request, 'user_edit.html', context)

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(admin_users)
    form = UserForm
    return render(request, 'add_user.html', {'form':form})

def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect(admin_users)


def add_main_category(request):
    form = MainCategoryForm(request.POST, request.FILES)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(admin_main_categories)
    return render(request, 'add_main_categories.html', context)

def edit_main_category(request, id):
    main_category = MainCategory.objects.get(id=id)
    form = CategoryForm(instance=main_category)
    if request.method == 'POST':
        form = MainCategoryForm(request.POST,instance=main_category)
        if form.is_valid():
            form.save()
            return redirect(admin_main_categories)
    context = {'form':form}
    return render(request, 'edit_main_category.html', context)

def delete_main_category(request, id):
    main_category = MainCategory.objects.get(id = id)
    main_category.delete()
    return redirect(admin_main_categories)


def edit_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect(admin_categories)
    context = {'form':form}
    return render(request, 'edit_category.html', context)

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(admin_categories)


def add_category(request):
    form = CategoryForm(request.POST, request.FILES)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(admin_categories)
    return render(request, 'add_category.html', context)


def edit_product(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect(admin_products)
    context = {'form':form}
    return render(request, 'edit_product.html', context)

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(admin_products)


def add_product(request):
    if request.method == 'POST':
        print('hey bro')
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(admin_products)
    form = ProductForm()
    return render(request, 'add_product.html', {'form':form})


def add_top_category(request):
    form = TopCategoryForm(request.POST)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(admin_top_categories)
    return render(request, 'add_top_category.html', context)

def edit_top_category(request, id):
    top_category = TopCategory.objects.get(id=id)
    form = TopCategoryForm(instance=top_category)
    if request.method == 'POST':
        form = TopCategoryForm(request.POST,instance=top_category)
        if form.is_valid():
            form.save()
            return redirect(admin_top_categories)
    context = {'form':form}
    return render(request, 'edit_top_category.html', context)

def delete_top_category(request, id):
    top_category = TopCategory.objects.get(id = id)
    top_category.delete()
    return redirect(admin_top_categories)


def edit_product_attributes(request, id):
    product = ProductAttribute.objects.get(id=id)
    form = ProductAttributeForm(instance=product)
    if request.method == 'POST':
        form = ProductAttributeForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect(admin_products_attributes)
    context = {'form':form}
    return render(request, 'edit_product_attributes.html', context)

def delete_product_attributes(request, id):
    product = ProductAttribute.objects.get(id=id)
    product.delete()
    return redirect(admin_products_attributes)


def add_product_attributes(request):
    if request.method == 'POST':
        print('hey bro')
        form = ProductAttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(admin_products_attributes)
    form = ProductAttributeForm()
    return render(request, 'add_product_attributes.html', {'form':form})


def admin_products_attributes(request):
    form = ProductAttribute.objects.all()
    context = {'form':form}
    return render(request, 'product_attributes.html', context)



def edit_order(request, id):
    order = CartOrder.objects.get(id=id)
    form = CartOrderForm(instance=order)
    if request.method == 'POST':
        form = CartOrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect(admin_orders)
    context = {'form':form}
    return render(request, 'edit_orders.html', context)

def delete_order(request, id):
    order = CartOrder.objects.get(id=id)
    order.delete()
    return redirect(admin_orders)



def edit_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    form = CouponForm(instance=coupon)
    if request.method == 'POST':
        form = CouponForm(request.POST,instance=coupon)
        if form.is_valid():
            form.save()
            return redirect(admin_coupons)
    context = {'form':form}
    return render(request, 'edit_coupons.html', context)

def delete_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect(admin_coupons)


def add_coupon(request):
    form = CouponForm(request.POST)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect(admin_coupons)
    return render(request, 'add_coupons.html', context)

def view_order_product(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {'products': products}
    return render(request, 'view_order_product.html', context)