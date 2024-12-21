import graphene
from graphql import GraphQLError
from services.models import ServiceCategory, ServiceSubCategory, ServiceTags
from site_api.schema_service.types import ServiceSubCategoryType, ServiceCategoryType
from site_api.schema_service.inputs import ServiceCategoryInput, ServiceSubCategoryInput
from site_api.schema_service.utils import get_category, get_subcategory

class CreateServiceCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceCategoryInput()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: ServiceCategoryType)

    def mutate(self, info:any, _input:ServiceCategoryInput) -> 'CreateServiceCategory':
        category = ServiceCategory(name=_input.name)
        category.save()
        return CreateServiceCategory(category=category, ok=True)


class CreateMultipleServiceCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceCategoryInput())

    ok = graphene.Boolean()
    categories = graphene.List(lambda: ServiceCategoryType)

    def mutate(self, info:any, inputs:list[ServiceCategoryInput]) -> 'CreateMultipleServiceCategories':
        categories = []
        for _input in inputs:
            category = ServiceCategory(name=_input.name)
            category.save()
            categories.append(category)
        return CreateMultipleServiceCategories(categories=categories, ok=True)


class UpdateServiceCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceCategoryInput()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: ServiceCategoryType)

    def mutate(self, info:any, _input:ServiceCategoryInput) -> 'UpdateServiceCategory':
        if (_input.name or _input.pk) is None or _input.new_name is None:
            raise GraphQLError('Fields: name or pk and new_name must be setted')  
        try:
            category = ServiceCategory.objects.get(pk=_input.pk)
        except ServiceCategory.DoesNotExist as e:
            raise GraphQLError("Category not found") from e
        category.name = _input.new_name
        category.save()
        return UpdateServiceCategory(category=category, ok=True)


class UpdateMultipleServiceCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceCategoryInput())

    ok = graphene.Boolean()
    categories = graphene.List(lambda: ServiceCategoryType)

    def mutate(self, info:any, inputs:list[ServiceCategoryInput]) -> 'UpdateMultipleServiceCategories':
        categories = []
        for _input in inputs:
            if (_input.name or _input.pk) is None or _input.new_name is None:
                raise GraphQLError('Fields: name, pk and new_name must be setted')  
            try:
                category = ServiceCategory.objects.get(pk=_input.pk)
            except ServiceCategory.DoesNotExist as e:
                raise GraphQLError("Category not found") from e
            category.name = _input.new_name
            category.save()
            categories.append(category)
        return UpdateMultipleServiceCategories(categores=categories, ok=True)


class DeleteServiceCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceCategoryInput()

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ServiceCategoryInput) -> 'DeleteServiceCategory':
        try:
            if _input.pk:
                category = ServiceCategory.objects.get(pk=_input.pk)
            else:
                category = ServiceCategory.objects.get(name=_input.name)
        except ServiceCategory.DoesNotExist as e:
            raise GraphQLError("Category not found") from e
        category.delete()
        return DeleteServiceCategory(ok=True)


class DeleteMultipleServiceCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceCategoryInput())

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ServiceCategoryInput]) -> 'DeleteMultipleServiceCategories':
        for _input in inputs:
            try:
                if _input.pk:
                    category = ServiceCategory.objects.get(pk=_input.pk)
                else:
                    category = ServiceCategory.objects.get(name=_input.name)
            except ServiceCategory.DoesNotExist as e:
                raise GraphQLError("Category not found") from e
            category.delete()
        return DeleteMultipleServiceCategories(ok=True)


class CreateServiceSubCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceSubCategoryInput(required=True)

    ok = graphene.Boolean()
    subcategory = graphene.Field(lambda: ServiceSubCategoryType)

    def mutate(self, info:any, _input:ServiceSubCategoryInput) -> 'CreateServiceSubCategory':
        category = get_category(_input)
        subcategory = ServiceSubCategory(
            name=_input.name,
            category=category
        )
        subcategory.save()
        return CreateServiceSubCategory(subcategory=subcategory, ok=True)



class CreateMultipleServiceSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceSubCategoryInput())

    ok = graphene.Boolean()
    subcategories = graphene.List(lambda: ServiceSubCategoryType)

    def mutate(self, info:any, inputs:list[ServiceSubCategoryInput]) -> 'CreateMultipleServiceSubCategories':
        subcategories = []
        for _input in inputs:
            category = get_category(_input)
            subcategory = ServiceSubCategory(
                name=_input.name,
                category=category
            )
            subcategory.save()
            subcategories.append(subcategory)
        return CreateMultipleServiceSubCategories(subcategories=subcategories, ok=True)


class UpdateServiceSubCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceSubCategoryInput(required=True)

    ok = graphene.Boolean()
    subcategory = graphene.Field(lambda: ServiceSubCategoryType)

    def mutate(self, info, _input:ServiceSubCategoryInput) -> 'UpdateServiceSubCategory':
        if (_input.name or _input.pk) is None or _input.new_name is None:
            raise GraphQLError('Fields name or pk and new_name must be setted')
        subcategory = get_subcategory(_input)
        subcategory.name = _input.new_name
        subcategory.save()
        return UpdateServiceSubCategory(subcategory=subcategory, ok=True)


class UpdateMultipleServiceSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceSubCategoryInput())

    ok = graphene.Boolean()
    subcategories = graphene.List(lambda: ServiceSubCategoryType)

    def mutate(self, info:any, inputs:list[ServiceSubCategoryInput]) -> 'UpdateMultipleServiceSubCategories':
        subcategories = []
        for _input in inputs:
            if (_input.name or _input.pk) is None or _input.new_name is None:
                raise GraphQLError('Fields name or pk and new_name must be setted')
            subcategory = get_subcategory(_input)
            subcategory.name = _input.new_name
            subcategory.save()
            subcategories.append(subcategory)
        return UpdateMultipleServiceSubCategories(subcategory=subcategory, ok=True)


class DeleteServiceSubCategory(graphene.Mutation):
    class Arguments:
        _input = ServiceSubCategoryInput()

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ServiceSubCategoryInput) -> 'DeleteServiceSubCategory':
        subcategory = get_subcategory(_input)
        subcategory.delete()
        return DeleteServiceSubCategory(ok=True)


class DeleteMultipleServiceSubCategories(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceSubCategoryInput())

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ServiceSubCategoryInput]) -> 'DeleteMultipleServiceSubCategories':
        for _input in inputs:
            subcategory = get_subcategory(_input)
            subcategory.delete()
        return DeleteMultipleServiceSubCategories(ok=True)


class DeleteServiceTag(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info:any, name:str) -> 'DeleteServiceTag':
        try:
            tag = ServiceTags.objects.get(name=name)
        except ServiceTags.DoesNotExist as e:
            raise GraphQLError("Tag not found") from e
        tag.delete()
        return DeleteServiceTag(ok=True)


class DeleteMultipleServiceTags(graphene.Mutation):
    class Arguments:
        names = graphene.List(graphene.String())

    ok = graphene.Boolean()

    def mutate(self, info:any, names:list[str]) -> 'DeleteMultipleServiceTags':
        for name in names:
            try:
                tag = ServiceTags.objects.get(name=name)
            except ServiceTags.DoesNotExist as e:
                raise GraphQLError("Tag not found") from e
            tag.delete()
        return DeleteMultipleServiceTags(ok=True)


class Mutation(graphene.ObjectType):
    create_service_category = CreateServiceCategory.Field()
    create_multiple_service_categories = CreateMultipleServiceCategories.Field()
    create_service_subcategory = CreateServiceSubCategory.Field()
    create_multiple_service_subcategories = CreateMultipleServiceSubCategories.Field()
    update_service_category = UpdateServiceCategory.Field()
    update_multiple_service_categories = UpdateMultipleServiceCategories.Field()
    update_service_subcategory = UpdateServiceSubCategory.Field()
    update_multiple_service_subcategories = UpdateMultipleServiceSubCategories.Field()
    delete_service_category = DeleteServiceCategory.Field()
    delete_multiple_service_category = DeleteMultipleServiceCategories.Field()
    delete_service_subcategory = DeleteServiceSubCategory.Field()
    delete_multiple_service_subcategories = DeleteMultipleServiceSubCategories.Field()
    delete_service_tag = DeleteServiceTag.Field()
    delete_multiple_service_tags = DeleteMultipleServiceTags.Field()