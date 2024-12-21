from dal import autocomplete
from services.models import Service, ServiceCategory, ServiceSubCategory, ServiceTags

class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Service.objects.all()
        if self.q:
            qs = qs.filter(title__icontains=self.q)
        return qs

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ServiceCategory.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ServiceSubCategory.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ServiceTags.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
