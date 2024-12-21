import graphene
from graphene_django.types import DjangoObjectType
from services.models import ServiceSection
from site_api.schema_service.graphene_inputs import ServiceSectionInput
from site_api.schema_service.utils import find_service, find_service_section, null_section,\
    validate_section_input, save_section


class ServiceSectionType(DjangoObjectType):
    class Meta:
        model = ServiceSection


class CreateServiceSection(graphene.Mutation):
    class Arguments:
        input = ServiceSectionInput(required=True)

    ok = graphene.Boolean()
    service_section = graphene.Field(lambda: ServiceSectionType)

    def mutate(self, info:any, _input: ServiceSectionInput) -> 'CreateServiceSection':
        _input = validate_section_input(_input)
        service = find_service(_input)
        service_section = save_section(_input, service=service)
        return CreateServiceSection(service_section=service_section, ok=True)


class CreateMultipleServiceSections(graphene.Mutation):
    class Arguments:
        inputs=graphene.List(ServiceSectionInput(required=True))

    ok = graphene.Boolean()
    service_sections = graphene.List(lambda: ServiceSectionType)

    def mutate(self, info:any, inputs:list[ServiceSectionInput]) -> 'CreateMultipleServiceSections':
        service_section_list=[]
        for _input in inputs:
            _input = validate_section_input(_input)
            service = find_service(_input)
            service_section = save_section(_input, service=service)
            service_section_list.append(service_section)
        return CreateMultipleServiceSections(service_sections=service_section_list, ok=True)



class UpdateServiceSection(graphene.Mutation):
    class Arguments:
        _input = ServiceSectionInput(required=True)

    service_section = graphene.Field(lambda: ServiceSectionType)
    ok = graphene.Boolean()

    def mutate(self, info:any, _input: ServiceSectionInput) -> 'UpdateServiceSection':
        _input = validate_section_input(_input)
        service_section = find_service_section(_input)
        service_section = null_section(service_section)
        service_section = save_section(_input, service_section)
        return UpdateServiceSection(service_section=service_section, ok=True)


class UpdateMultipleServiceSections(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceSectionInput)

    service_sections = graphene.List(lambda: ServiceSectionType)
    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ServiceSectionInput]) -> 'UpdateMultipleServiceSections':
        service_sections = []
        for _input in inputs:
            _input = validate_section_input(_input)
            service_section = find_service_section(_input)
            service_section = null_section(service_section)
            service_section = save_section(_input, service_section)
            service_sections.append(service_section)
        return UpdateMultipleServiceSections(service_sections=service_sections, ok=True)


class DeleteServiceSection(graphene.Mutation):
    class Arguments:
        _input = ServiceSectionInput(required=True)

    ok = graphene.Boolean()

    def mutate(self, info:any, _input:ServiceSectionInput) -> 'DeleteServiceSection':
        service_section = find_service_section(_input)
        service_section.delete()
        return DeleteServiceSection(ok=True)


class DeleteMultipleServiceSections(graphene.Mutation):
    class Arguments:
        inputs = graphene.List(ServiceSectionInput)

    ok = graphene.Boolean()

    def mutate(self, info:any, inputs:list[ServiceSectionInput]) -> 'DeleteMultipleServiceSections':
        for _input in inputs:
            service_section = find_service_section(_input)
            service_section.delete()
        return DeleteMultipleServiceSections(ok=True)


class ServiceMutation(graphene.ObjectType):
    create_service_section = CreateServiceSection.Field()
    create_multiple_services = CreateMultipleServiceSections.Field()
    update_service = UpdateServiceSection.Field()
    update_multiple_services = UpdateMultipleServiceSections.Field()
    delete_service = DeleteServiceSection.Field()
    delete_multiple_services = DeleteMultipleServiceSections.Field()