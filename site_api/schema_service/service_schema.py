import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from services.models import Service, ServiceTags, ServiceSubCategory, ServiceCategory
from site_api.utils import save_obj
from site_api.schema_service.graphene_inputs import ServiceInput
from site_api.schema_service.utils import save_service, validate_input_cat_subcat, add_tags, find_service, remove_tags


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class CreateService(graphene.Mutation):
    class Arguments:
        _input = ServiceInput(required=True)

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info:any, _input: ServiceInput) -> 'CreateService':
        if Service.objects.filter(title=_input.service_title).exists():
            raise GraphQLError("Service with this title already exists.")
        if bool(_input.preview_video_url) == bool(_input.preview_image):
            raise GraphQLError("Either preview_video_url or preview_image must be provided, but not both.")
        category, subcategory = validate_input_cat_subcat(_input) 
        service = save_service(_input, category=category, subcategory=subcategory)
        service = add_tags(_input, service)
        service = remove_tags(_input, service)
        return CreateService(service=service, ok=True)


class CreateMultipleServices(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceInput())

    ok = graphene.Boolean()
    services = graphene.List(lambda: ServiceType)

    def mutate(self, info:any, inputs:list[ServiceInput]) -> 'CreateMultipleServices':
        services = []
        for _input in inputs:
            if Service.objects.filter(title=_input.service_title).exists():
                raise GraphQLError("Service with this title already exists.")
            category, subcategory = validate_input_cat_subcat(_input) 
            service = save_service(_input, category=category, subcategory=subcategory)
            service = add_tags(_input, service)
            services.append(service)
        return CreateMultipleServices(services=services, ok=True)


class UpdateService(graphene.Mutation):
    class Arguments:
        _input = ServiceInput()

    service = graphene.Field(lambda: ServiceType)
    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ServiceInput) -> 'UpdateService': 
        if _input.preview_video_url and _input.preview_image:
            raise GraphQLError("Both preview_video_url and preview_image cannot be provided simultaneously.")
        service = find_service(_input)
        category, subcategory = validate_input_cat_subcat(_input)
        service = save_service(_input, service, category, subcategory)
        service = add_tags(_input, service)
        return UpdateService(service=service, ok=True)


class UpdateMultipleServices(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceInput())

    services = graphene.List(lambda: ServiceType)
    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ServiceInput]) -> 'UpdateMultipleServices':
        services = []
        for _input in inputs:
            if _input.preview_video_url and _input.preview_image:
                raise GraphQLError("Both preview_video_url and preview_image cannot be provided simultaneously.")
            service = find_service(_input)
            category, subcategory = validate_input_cat_subcat(_input)
            service = save_service(_input, service, category, subcategory)
            service = add_tags(_input, service)
            services.append(service)
        return UpdateMultipleServices(services=services, ok=True)


class DeleteService(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()
        title = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info:any, pk:int=None, title:str=None) -> 'DeleteService':
        try:
            if pk:
                service = Service.objects.get(pk=pk)
            elif title:
                service = Service.objects.get(title=title)
        except Service.DoesNotExist as e:
            raise GraphQLError("Service not found.") from e
        service.delete()
        return DeleteService(ok=True)


class DeleteMultipleServices(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.Int)
        titles = graphene.List(graphene.String)

    ok = graphene.Boolean()

    def mutate(self, info:any, ids:list[int]=None, titles:list[str]=None) -> 'DeleteMultipleServices':
        if ids:
            Service.objects.filter(pk__in=ids).delete()
        if titles:
            Service.objects.filter(title__in=titles).delete()
        return DeleteMultipleServices(ok=True)


class ServiceMutation(graphene.ObjectType):
    create_service = CreateService.Field()
    create_multiple_services = CreateMultipleServices.Field()
    update_service = UpdateService.Field()
    update_multiple_services = UpdateMultipleServices.Field()
    delete_service = DeleteService.Field()
    delete_multiple_services = DeleteMultipleServices.Field()