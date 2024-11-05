from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dal import autocomplete
from .models import UserProfile, Product, CommercialOffer, OfferProduct, Decoration

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'position', 'signature']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'article', 'tags', 'photo']

class CommercialOfferForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='product-autocomplete')
    )

    class Meta:
        model = CommercialOffer
        fields = ['organization', 'products', 'delivery_time', 'user', 'decoration']

class OfferProductForm(forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = ['product', 'quantity', 'price_per_unit']

class DecorationForm(forms.ModelForm):
    class Meta:
        model = Decoration
        fields = ['name', 'image']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')