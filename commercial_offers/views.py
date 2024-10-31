from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CommercialOffer, Product
from .forms import CommercialOfferForm, ProductForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def commercial_offers_list(request):
    offers = CommercialOffer.objects.filter(user=request.user.userprofile)
    return render(request, 'commercial_offers_list.html', {'offers': offers})

@login_required
def create_commercial_offer(request):
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user.userprofile
            offer.save()
            return redirect('commercial_offers_list')
    else:
        form = CommercialOfferForm()
    return render(request, 'create_commercial_offer.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

@login_required
def edit_commercial_offer(request, pk):
    offer = CommercialOffer.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommercialOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('commercial_offers_list')
    else:
        form = CommercialOfferForm(instance=offer)
    return render(request, 'edit_commercial_offer.html', {'form': form})

@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})

def generate_pdf(request, pk):
    offer = CommercialOffer.objects.get(pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="offer_{offer.number}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Commercial Offer {offer.number}")
    p.drawString(100, 730, f"Date: {offer.date}")
    p.drawString(100, 710, f"Organization: {offer.organization.name}")
    p.drawString(100, 690, f"Recipient: {offer.recipient}")
    p.drawString(100, 670, f"Delivery Time: {offer.delivery_time}")

    y = 650
    for product in offer.products.all():
        p.drawString(100, y, f"Product: {product.name}")
        p.drawString(100, y - 20, f"Quantity: {product.quantity}")
        p.drawString(100, y - 40, f"Price per Unit: {product.price_per_unit}")
        p.drawString(100, y - 60, f"Total Price: {product.total_price}")
        y -= 80

    p.showPage()
    p.save()
    return response

def print_offer(request, pk):
    offer = CommercialOffer.objects.get(pk=pk)
    template = get_template('print_offer.html')
    context = {'offer': offer}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="offer_{offer.number}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Commercial Offer {offer.number}")
    p.drawString(100, 730, f"Date: {offer.date}")
    p.drawString(100, 710, f"Organization: {offer.organization.name}")
    p.drawString(100, 690, f"Recipient: {offer.recipient}")
    p.drawString(100, 670, f"Delivery Time: {offer.delivery_time}")

    y = 650
    for product in offer.products.all():
        p.drawString(100, y, f"Product: {product.name}")
        p.drawString(100, y - 20, f"Quantity: {product.quantity}")
        p.drawString(100, y - 40, f"Price per Unit: {product.price_per_unit}")
        p.drawString(100, y - 60, f"Total Price: {product.total_price}")
        y -= 80

    p.showPage()
    p.save()
    return response

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})