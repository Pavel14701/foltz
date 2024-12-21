import graphene
from graphql import GraphQLError
from products.models import ProductCategory, ProductSubCategory, ProductTags
from site_api.schema_product.types import ProductSubCategoryType, ProductCategoryType
from site_api.schema_product.inputs import ProductCategoryInput, ProductSubCategoryInput
from site_api.schema_product.utils import get_category, get_subcategory

class CreateProductCategory(graphene.Mutation):
    class Arguments:
        _input = ProductCategoryInput()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: ProductCategoryType)

    def mutate(self, info:any, _input:ProductCategoryInput) -> 'CreateProductCategory':
        category = ProductCategory(name=_input.name)
        category.save()
        return CreateProductCategory(category=category, ok=True)


class CreateMultipleProductCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductCategoryInput())

    ok = graphene.Boolean()
    categories = graphene.List(lambda: ProductCategoryType)

    def mutate(self, info:any, inputs:list[ProductCategoryInput]) -> 'CreateMultipleProductCategories':
        categories = []
        for _input in inputs:
            category = ProductCategory(name=_input.name)
            category.save()
            categories.append(category)
        return CreateMultipleProductCategories(categories=categories, ok=True)


class UpdateProductCategory(graphene.Mutation):
    class Arguments:
        _input = ProductCategoryInput()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: ProductCategoryType)

    def mutate(self, info:any, _input:ProductCategoryInput) -> 'UpdateProductCategory':
        if (_input.name or _input.pk) is None or _input.new_name is None:
            raise GraphQLError('Fields: name or pk and new_name must be setted')  
        try:
            category = ProductCategory.objects.get(pk=_input.pk)
        except ProductCategory.DoesNotExist as e:
            raise GraphQLError("Category not found") from e
        category.name = _input.new_name
        category.save()
        return UpdateProductCategory(category=category, ok=True)


class UpdateMultipleProductCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductCategoryInput())

    ok = graphene.Boolean()
    categories = graphene.List(lambda: ProductCategoryType)

    def mutate(self, info:any, inputs:list[ProductCategoryInput]) -> 'UpdateMultipleProductCategories':
        categories = []
        for _input in inputs:
            if (_input.name or _input.pk) is None or _input.new_name is None:
                raise GraphQLError('Fields: name, pk and new_name must be setted')  
            try:
                category = ProductCategory.objects.get(pk=_input.pk)
            except ProductCategory.DoesNotExist as e:
                raise GraphQLError("Category not found") from e
            category.name = _input.new_name
            category.save()
            categories.append(category)
        return UpdateMultipleProductCategories(categores=categories, ok=True)


class DeleteProductCategory(graphene.Mutation):
    class Arguments:
        _input = ProductCategoryInput()

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ProductCategoryInput) -> 'DeleteProductCategory':
        try:
            if _input.pk:
                category = ProductCategory.objects.get(pk=_input.pk)
            else:
                category = ProductCategory.objects.get(name=_input.name)
        except ProductCategory.DoesNotExist as e:
            raise GraphQLError("Category not found") from e
        category.delete()
        return DeleteProductCategory(ok=True)


class DeleteMultipleProductCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductCategoryInput())

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ProductCategoryInput]) -> 'DeleteMultipleProductCategories':
        for _input in inputs:
            try:
                if _input.pk:
                    category = ProductCategory.objects.get(pk=_input.pk)
                else:
                    category = ProductCategory.objects.get(name=_input.name)
            except ProductCategory.DoesNotExist as e:
                raise GraphQLError("Category not found") from e
            category.delete()
        return DeleteMultipleProductCategories(ok=True)


class CreateProductSubCategory(graphene.Mutation):
    class Arguments:
        _input = ProductSubCategoryInput(required=True)

    ok = graphene.Boolean()
    subcategory = graphene.Field(lambda: ProductSubCategoryType)

    def mutate(self, info:any, _input:ProductSubCategoryInput) -> 'CreateProductSubCategory':
        category = get_category(_input)
        subcategory = ProductSubCategory(
            name=_input.name,
            category=category
        )
        subcategory.save()
        return CreateProductSubCategory(subcategory=subcategory, ok=True)



class CreateMultipleProductSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductSubCategoryInput())

    ok = graphene.Boolean()
    subcategories = graphene.List(lambda: ProductSubCategoryType)

    def mutate(self, info:any, inputs:list[ProductSubCategoryInput]) -> 'CreateMultipleProductSubCategories':
        subcategories = []
        for _input in inputs:
            category = get_category(_input)
            subcategory = ProductSubCategory(
                name=_input.name,
                category=category
            )
            subcategory.save()
            subcategories.append(subcategory)
        return CreateMultipleProductSubCategories(subcategories=subcategories, ok=True)


class UpdateProductSubCategory(graphene.Mutation):
    class Arguments:
        _input = ProductSubCategoryInput(required=True)

    ok = graphene.Boolean()
    subcategory = graphene.Field(lambda: ProductSubCategoryType)

    def mutate(self, info, _input:ProductSubCategoryInput) -> 'UpdateProductSubCategory':
        if (_input.name or _input.pk) is None or _input.new_name is None:
            raise GraphQLError('Fields name or pk and new_name must be setted')
        subcategory = get_subcategory(_input)
        subcategory.name = _input.new_name
        subcategory.save()
        return UpdateProductSubCategory(subcategory=subcategory, ok=True)


class UpdateMultipleProductSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductSubCategoryInput())

    ok = graphene.Boolean()
    subcategories = graphene.List(lambda: ProductSubCategoryType)

    def mutate(self, info:any, inputs:list[ProductSubCategoryInput]) -> 'UpdateMultipleProductSubCategories':
        subcategories = []
        for _input in inputs:
            if (_input.name or _input.pk) is None or _input.new_name is None:
                raise GraphQLError('Fields name or pk and new_name must be setted')
            subcategory = get_subcategory(_input)
            subcategory.name = _input.new_name
            subcategory.save()
            subcategories.append(subcategory)
        return UpdateMultipleProductSubCategories(subcategory=subcategory, ok=True)


class DeleteProductSubCategory(graphene.Mutation):
    class Arguments:
        _input = ProductSubCategoryInput()

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ProductSubCategoryInput) -> 'DeleteProductSubCategory':
        subcategory = get_subcategory(_input)
        subcategory.delete()
        return DeleteProductSubCategory(ok=True)


class DeleteMultipleProductSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductSubCategoryInput())

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ProductSubCategoryInput]) -> 'DeleteMultipleProductSubCategories':
        for _input in inputs:
            subcategory = get_subcategory(_input)
            subcategory.delete()
        return DeleteMultipleProductSubCategories(ok=True)


class DeleteProductTag(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info:any, name:str) -> 'DeleteProductTag':
        try:
            tag = ProductTags.objects.get(name=name)
        except ProductTags.DoesNotExist as e:
            raise GraphQLError("Tag not found") from e
        tag.delete()
        return DeleteProductTag(ok=True)


class DeleteMultipleProductTags(graphene.Mutation):
    class Arguments:
        names = graphene.List(graphene.String())

    ok = graphene.Boolean()

    def mutate(self, info:any, names:list[str]) -> 'DeleteMultipleProductTags':
        for name in names:
            try:
                tag = ProductTags.objects.get(name=name)
            except ProductTags.DoesNotExist as e:
                raise GraphQLError("Tag not found") from e
            tag.delete()
        return DeleteMultipleProductTags(ok=True)


class Mutation(graphene.ObjectType):
    create_product_category = CreateProductCategory.Field()
    create_multiple_product_categories = CreateMultipleProductCategories.Field()
    create_product_subcategory = CreateProductSubCategory.Field()
    create_multiple_product_subcategories = CreateMultipleProductSubCategories.Field()
    update_product_category = UpdateProductCategory.Field()
    update_multiple_product_categories = UpdateMultipleProductCategories.Field()
    update_product_subcategory = UpdateProductSubCategory.Field()
    update_multiple_product_subcategories = UpdateMultipleProductSubCategories.Field()
    delete_product_category = DeleteProductCategory.Field()
    delete_multiple_product_category = DeleteMultipleProductCategories.Field()
    delete_product_subcategory = DeleteProductSubCategory.Field()
    delete_multiple_product_subcategories = DeleteMultipleProductSubCategories.Field()
    delete_product_tag = DeleteProductTag.Field()
    delete_multiple_product_tags = DeleteMultipleProductTags.Field()