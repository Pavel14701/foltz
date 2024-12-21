from graphene_django import DjangoObjectType
from products.models import Product, ProductCategory, ProductSubCategory,\
    ProductTags, ProductSection


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory


class ProductSubCategoryType(DjangoObjectType):
    class Meta:
        model = ProductSubCategory


class ProductTagsType(DjangoObjectType):
    class Meta:
        model = ProductTags


class ProductSectionType(DjangoObjectType):
    class Meta:
        model = ProductSection


class ProductType(DjangoObjectType):
    class Meta:
        model = Product