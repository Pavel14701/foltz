import hashlib
from django.http import JsonResponse, HttpResponseNotModified,\
    HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import http_date
from django.views import View
from site_forms.custom_form import ContactForm
from services.models import Service, ServiceCategory, ServiceSubCategory, ServiceTags
from common.dto import FormData
from common.aplications import SendAplications


class ServiceFormView(View):
    def form_view(self, request:HttpRequest) -> HttpResponseRedirect|HttpResponse:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form_data = FormData(
                    name = form.cleaned_data['name'],
                    phone = form.cleaned_data['phone'],
                    question = form.cleaned_data['question']
                )
                sendler = SendAplications(form_data)
                sendler.email()
                sendler.tg()
                return redirect('success')
        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})


class ServicesViews(View):
    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse|HttpResponseNotModified|JsonResponse: 
        action = kwargs.pop('action', None) 
        if action == 'get_service':
            return self.get_service(request, *args, **kwargs) 
        elif action == 'get_service_details':
            return self.get_service_details(request, *args, **kwargs)
        elif action == 'service_search': 
            return self.service_search(request, *args, **kwargs) 
        elif action == 'home_view':
            return self.home_view(request, *args, **kwargs)


    def get_service(self, request:HttpRequest, *args, **kwargs) -> JsonResponse:
        service = Service.objects.get(pk=kwargs['pk'])
        content = {
            'title': service.title,
            'preview_image': service.preview_image.url if service.preview_image else None,
            'price': service.price
        }
        etag_content = f"{service.title}-{service.preview_image}-{service.price}"
        etag = hashlib.md5(etag_content.encode('utf-8')).hexdigest()
        if_none_match = request.headers.get('If-None-Match')
        if if_none_match == etag:
            return HttpResponseNotModified()
        response = JsonResponse(content)
        response['ETag'] = etag
        last_modified = service.modified
        response['Last-Modified'] = http_date(last_modified.timestamp())
        return response


    def get_service_details(self, request:HttpRequest, *args, **kwargs) -> HttpResponseNotModified|HttpResponse:
        service = get_object_or_404(Service, pk=kwargs['pk'])
        sections = service.service_section.all()
        etag_content = f"{service.title}-{service.preview_image}-{service.price}-{service.modified}"
        etag = hashlib.md5(etag_content.encode('utf-8')).hexdigest()
        if_none_match = request.headers.get('If-None-Match')
        if if_none_match == etag:
            return HttpResponseNotModified()
        last_modified = service.modified
        context = {
            'service': service,
            'sections': sections,
            'tags': service.tags.all(),
            'category': service.category
        }
        response = render(request, 'services/detail.html', context)
        response['ETag'] = etag
        response['Last-Modified'] = http_date(last_modified.timestamp())
        return response


    #TO DO Add subcategory in filter
    def service_search(self, request:HttpRequest) -> HttpResponse:
        title_query = request.GET.get('title', '')
        category_query = request.GET.get('category', '')
        tag_query = request.GET.get('tag', '')
        services = Service.objects.all()
        search_performed = False
        if title_query:
            services = services.filter(title__icontains=title_query)
            search_performed = True
        if category_query:
            services = services.filter(category__name__icontains=category_query)
            search_performed = True
        if tag_query:
            services = services.filter(tags__name__icontains=tag_query)
            search_performed = True
        context = {'services': services, 'search_performed': search_performed}
        return render(request, 'services/base.html', context)


    #TO DO Add subcategory in filter
    def home_view(self, request: HttpRequest) -> HttpResponseNotModified | HttpResponse:
        title_query = request.GET.get('title', '')
        category_query = request.GET.get('category', '')
        tag_query = request.GET.get('tag', '')
        services_by_category = {}
        search_performed = False
        categories = ServiceCategory.objects.all()
        page_number = request.GET.get('page')
        if title_query or category_query or tag_query:
            search_performed = True
            services = Service.objects.all()
            if title_query:
                services = services.filter(title__icontains=title_query)
            if category_query:
                services = services.filter(category__name__icontains=category_query)
            if tag_query:
                services = services.filter(tags__name__icontains=tag_query)
        else:
            for category in categories:
                services = Service.objects.filter(category=category)[:4]
                services_by_category[category] = services
            paginator = Paginator(categories, 1)
            page_obj = paginator.get_page(page_number)
        etag_content = f"{title_query}-{category_query}-{tag_query}-{page_number}"
        etag = hashlib.md5(etag_content.encode('utf-8')).hexdigest()
        if_none_match = request.headers.get('If-None-Match')
        if if_none_match == etag:
            return HttpResponseNotModified()
        if not search_performed and categories.exists():
            last_modified = categories.latest('modified').modified
        elif search_performed and services.exists():
            last_modified = services.latest('modified').modified
        else:
            last_modified = None
        context = {
            'services_by_category': services_by_category,
            'page_obj': None if search_performed else page_obj,
            'services': services if search_performed else None,
            'search_performed': search_performed
        }
        response = render(request, 'services/base.html', context)
        response['ETag'] = etag
        if last_modified:
            response['Last-Modified'] = http_date(last_modified.timestamp())
        return response