import graphene
from products.models import Product, ProductSubCategory, ProductCategory
from site_api.schema_product.types import ProductType, ProductSubCategoryType,\
    ProductCategoryType


class ProductQuery(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        product_ids=graphene.List(graphene.ID),
        product_titles=graphene.List(graphene.String)
    )
    product = graphene.Field(
        ProductType, product_id=graphene.ID(), product_title=graphene.String()
    ) 
    subcategories = graphene.List(
        ProductSubCategoryType, category_id=graphene.ID(), category_name=graphene.String()
    )
    products_by_category = graphene.List(
        ProductType, category_name=graphene.String(), subcategory_name=graphene.String()
    )
    products_by_tags = graphene.List(ProductType, tag_names=graphene.List(graphene.String))
    categories = graphene.List(ProductCategoryType)

    def resolve_products(self, info:any, product_ids:list[int]=None, product_titles:list[str]=None) -> list[Product]:
        if product_ids:
            return Product.objects.filter(pk__in=product_ids)
        if product_titles:
            return Product.objects.filter(title__in=product_titles)
        return Product.objects.all()

    def resolve_product(self, info:any, product_id:int=None, product_title:str=None) -> Product:
        if product_id:
            return Product.objects.get(pk=product_id)
        return Product.objects.get(title=product_title) if product_title else None

    def resolve_categories(self, info:any) -> list[ProductCategory]:
        return ProductCategory.objects.all()

    def resolve_subcategories(self, info:any, category_id:int=None, category_name:str=None) -> list[ProductSubCategory]:
        if category_id:
            return ProductSubCategory.objects.filter(category_id=category_id)
        if category_name:
            category = ProductCategory.objects.get(name=category_name)
            return ProductSubCategory.objects.filter(category=category)
        return ProductSubCategory.objects.all()

    def resolve_products_by_category(self, info:any, category_name:str, subcategory_name:str=None) -> list|list[Product]:
        if not category_name:
            return Product.objects.all()
        try:
            category = ProductCategory.objects.get(name=category_name)
        except ProductCategory.DoesNotExist:
            return []
        if subcategory_name:
            try:
                subcategory = ProductSubCategory.objects.get(name=subcategory_name, category=category)
                return Product.objects.filter(category=category, subcategory=subcategory)
            except ProductSubCategory.DoesNotExist:
                return []
        return Product.objects.filter(category=category)

    def resolve_products_by_tags(self, info:any, tag_names:list[str]=None) -> list[Product]:
        if tag_names: 
            return Product.objects.filter(tags__name__in=tag_names).distinct()
        return Product.objects.all()
