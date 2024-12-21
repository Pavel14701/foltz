from dal import autocomplete
from products.models import Product, ProductCategory, ProductSubCategory, ProductTags

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProductCategory.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProductSubCategory.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ProductTags.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
