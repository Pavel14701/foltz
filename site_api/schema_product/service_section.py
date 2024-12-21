import graphene
from graphene_django.types import DjangoObjectType
from products.models import ProductSection
from site_api.schema_product.inputs import ProductSectionInput
from site_api.schema_product.utils import find_product, find_product_section, null_section,\
    validate_section_input, save_section


class ProductSectionType(DjangoObjectType):
    class Meta:
        model = ProductSection


class CreateProductSection(graphene.Mutation):
    class Arguments:
        input = ProductSectionInput(required=True)

    ok = graphene.Boolean()
    product_section = graphene.Field(lambda: ProductSectionType)

    def mutate(self, info:any, _input: ProductSectionInput) -> 'CreateProductSection':
        _input = validate_section_input(_input)
        product = find_product(_input)
        product_section = save_section(_input, product=product)
        return CreateProductSection(product_section=product_section, ok=True)


class CreateMultipleProductSections(graphene.Mutation):
    class Arguments:
        inputs=graphene.List(ProductSectionInput(required=True))

    ok = graphene.Boolean()
    product_sections = graphene.List(lambda: ProductSectionType)

    def mutate(self, info:any, inputs:list[ProductSectionInput]) -> 'CreateMultipleProductSections':
        product_section_list=[]
        for _input in inputs:
            _input = validate_section_input(_input)
            product = find_product(_input)
            product_section = save_section(_input, product=product)
            product_section_list.append(product_section)
        return CreateMultipleProductSections(product_sections=product_section_list, ok=True)



class UpdateProductSection(graphene.Mutation):
    class Arguments:
        _input = ProductSectionInput(required=True)

    product_section = graphene.Field(lambda: ProductSectionType)
    ok = graphene.Boolean()

    def mutate(self, info:any, _input: ProductSectionInput) -> 'UpdateProductSection':
        _input = validate_section_input(_input)
        product_section = find_product_section(_input)
        product_section = null_section(product_section)
        product_section = save_section(_input, product_section)
        return UpdateProductSection(product_section=product_section, ok=True)


class UpdateMultipleProductSections(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductSectionInput)

    product_sections = graphene.List(lambda: ProductSectionType)
    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ProductSectionInput]) -> 'UpdateMultipleProductSections':
        product_sections = []
        for _input in inputs:
            _input = validate_section_input(_input)
            product_section = find_product_section(_input)
            product_section = null_section(product_section)
            product_section = save_section(_input, product_section)
            product_sections.append(product_section)
        return UpdateMultipleProductSections(product_sections=product_sections, ok=True)


class DeleteProductSection(graphene.Mutation):
    class Arguments:
        _input = ProductSectionInput(required=True)

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ProductSectionInput) -> 'DeleteProductSection':
        product_section = find_product_section(_input)
        product_section.delete()
        return DeleteProductSection(ok=True)


class DeleteMultipleProductSections(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ProductSectionInput)

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ProductSectionInput]) -> 'DeleteMultipleProductSections':
        for _input in inputs:
            product_section = find_product_section(_input)
            product_section.delete()
        return DeleteMultipleProductSections(ok=True)


class ProductSectionMutation(graphene.ObjectType):
    create_product_section = CreateProductSection.Field()
    create_multiple_products = CreateMultipleProductSections.Field()
    update_product = UpdateProductSection.Field()
    update_multiple_products = UpdateMultipleProductSections.Field()
    delete_product = DeleteProductSection.Field()
    delete_multiple_products = DeleteMultipleProductSections.Field()