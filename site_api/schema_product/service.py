import graphene
from graphql import GraphQLError
from products.models import Product
from site_api.schema_product.inputs import ProductInput
from site_api.schema_product.types import ProductType
from site_api.schema_product.utils import save_product,\
    validate_input_cat_subcat, add_tags, find_product, remove_tags



class CreateProduct(graphene.Mutation):
    class Arguments:
        _input = ProductInput(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: ProductType)

    def mutate(self, info:any, _input: ProductInput) -> 'CreateProduct':
        if Product.objects.filter(title=_input.product_title).exists():
            raise GraphQLError(
                "Product with this\
                title already exists."
            )
        if bool(_input.preview_video_url) == bool(_input.preview_image):
            raise GraphQLError(
                "Either preview_video_url \
                or preview_image must be \
                provided, but not both."
            )
        category, subcategory = validate_input_cat_subcat(_input) 
        product = save_product(_input, category=category, subcategory=subcategory)
        product = add_tags(_input, product)
        product = remove_tags(_input, product)
        return CreateProduct(product=product, ok=True)


class CreateMultipleProducts(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductInput())

    ok = graphene.Boolean()
    products = graphene.List(lambda: ProductType)

    def mutate(self, info:any, inputs:list[ProductInput]) -> 'CreateMultipleProducts':
        products = []
        for _input in inputs:
            if Product.objects.filter(title=_input.product_title).exists():
                raise GraphQLError(
                    "Product with this \
                    title already exists."
                )
            category, subcategory = validate_input_cat_subcat(_input) 
            product = save_product(_input, category=category, subcategory=subcategory)
            product = add_tags(_input, product)
            products.append(product)
        return CreateMultipleProducts(products=products, ok=True)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        _input = ProductInput()

    product = graphene.Field(lambda: ProductType)
    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ProductInput) -> 'UpdateProduct': 
        if _input.preview_video_url and _input.preview_image:
            raise GraphQLError(
                "Both preview_video_url and \
                preview_image cannot be \
                provided simultaneously."
            )
        product = find_product(_input)
        category, subcategory = validate_input_cat_subcat(_input)
        product = save_product(_input, product, category, subcategory)
        product = add_tags(_input, product)
        return UpdateProduct(product=product, ok=True)


class UpdateMultipleProducts(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductInput())

    products = graphene.List(lambda: ProductType)
    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ProductInput]) -> 'UpdateMultipleProducts':
        products = []
        for _input in inputs:
            if _input.preview_video_url and _input.preview_image:
                raise GraphQLError(
                    "Both preview_video_url \
                    and preview_image cannot \
                    be provided simultaneously."
                )
            product = find_product(_input)
            category, subcategory = validate_input_cat_subcat(_input)
            product = save_product(_input, product, category, subcategory)
            product = add_tags(_input, product)
            products.append(product)
        return UpdateMultipleProducts(products=products, ok=True)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()
        title = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info:any, pk:int=None, title:str=None) -> 'DeleteProduct':
        try:
            if pk:
                product = Product.objects.get(pk=pk)
            elif title:
                product = Product.objects.get(title=title)
        except Product.DoesNotExist as e:
            raise GraphQLError("Product not found.") from e
        product.delete()
        return DeleteProduct(ok=True)


class DeleteMultipleProducts(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.Int)
        titles = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info:any, ids:list[int]=None, titles:list[str]=None) -> 'DeleteMultipleProducts':
        if ids:
            Product.objects.filter(pk__in=ids).delete()
        if titles:
            Product.objects.filter(title__in=titles).delete()
        return DeleteMultipleProducts(ok=True)


class ProductMutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_multiple_products = CreateMultipleProducts.Field()
    update_product = UpdateProduct.Field()
    update_multiple_products = UpdateMultipleProducts.Field()
    delete_product = DeleteProduct.Field()
    delete_multiple_products = DeleteMultipleProducts.Field()