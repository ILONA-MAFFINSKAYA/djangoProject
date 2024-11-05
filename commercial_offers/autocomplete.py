from dal import autocomplete
from .models import Product

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q) | qs.filter(article__icontains=self.q) | qs.filter(tags__icontains=self.q)

        return qs