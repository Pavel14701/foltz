import graphene
from services.models import Service, ServiceSubCategory, ServiceCategory
from site_api.schema_service.types import ServiceType, ServiceSubCategoryType,\
    ServiceCategoryType


class ServiceQuery(graphene.ObjectType):
    services = graphene.List(
        ServiceType,
        service_ids=graphene.List(graphene.ID),
        service_titles=graphene.List(graphene.String)
    )
    service = graphene.Field(
        ServiceType, service_id=graphene.ID(), service_title=graphene.String()
    ) 
    subcategories = graphene.List(
        ServiceSubCategoryType, category_id=graphene.ID(), category_name=graphene.String()
    )
    services_by_category = graphene.List(
        ServiceType, category_name=graphene.String(), subcategory_name=graphene.String()
    )
    services_by_tags = graphene.List(ServiceType, tag_names=graphene.List(graphene.String))
    categories = graphene.List(ServiceCategoryType)

    def resolve_services(self, info:any, service_ids:list[int]=None, service_titles:list[str]=None) -> list[Service]:
        if service_ids:
            return Service.objects.filter(pk__in=service_ids)
        if service_titles:
            return Service.objects.filter(title__in=service_titles)
        return Service.objects.all()

    def resolve_service(self, info:any, service_id:int=None, service_title:str=None) -> Service:
        if service_id:
            return Service.objects.get(pk=service_id)
        return Service.objects.get(title=service_title) if service_title else None

    def resolve_categories(self, info:any) -> list[ServiceCategory]:
        return ServiceCategory.objects.all()

    def resolve_subcategories(self, info:any, category_id:int=None, category_name:str=None) -> list[ServiceSubCategory]:
        if category_id:
            return ServiceSubCategory.objects.filter(category_id=category_id)
        if category_name:
            category = ServiceCategory.objects.get(name=category_name)
            return ServiceSubCategory.objects.filter(category=category)
        return ServiceSubCategory.objects.all()

    def resolve_services_by_category(self, info:any, category_name:str, subcategory_name:str=None) -> list|list[Service]:
        if not category_name:
            return Service.objects.all()
        try:
            category = ServiceCategory.objects.get(name=category_name)
        except ServiceCategory.DoesNotExist:
            return []
        if subcategory_name:
            try:
                subcategory = ServiceSubCategory.objects.get(name=subcategory_name, category=category)
                return Service.objects.filter(category=category, subcategory=subcategory)
            except ServiceSubCategory.DoesNotExist:
                return []
        return Service.objects.filter(category=category)

    def resolve_services_by_tags(self, info:any, tag_names:list[str]=None) -> list[Service]:
        if tag_names: 
            return Service.objects.filter(tags__name__in=tag_names).distinct()
        return Service.objects.all()
