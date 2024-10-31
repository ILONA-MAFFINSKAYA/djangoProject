from django.contrib import admin
from .models import UserProfile, Organization, Product, CommercialOffer, OfferProduct, Decoration

admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Product)
admin.site.register(CommercialOffer)
admin.site.register(OfferProduct)
admin.site.register(Decoration)
