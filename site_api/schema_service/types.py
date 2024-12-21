from graphene_django import DjangoObjectType
from services.models import Service, ServiceCategory, ServiceSubCategory,\
    ServiceTags, ServiceSection


class ServiceCategoryType(DjangoObjectType):
    class Meta:
        model = ServiceCategory


class ServiceSubCategoryType(DjangoObjectType):
    class Meta:
        model = ServiceSubCategory


class ServiceTagsType(DjangoObjectType):
    class Meta:
        model = ServiceTags


class ServiceSectionType(DjangoObjectType):
    class Meta:
        model = ServiceSection


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service