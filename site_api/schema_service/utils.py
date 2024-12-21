from services.models import ServiceSection, Service, ServiceCategory, ServiceSubCategory, ServiceTags
from graphql import GraphQLError
from site_api.schema_service.inputs import ServiceSectionInput, ServiceInput, ServiceSubCategoryInput


def find_service(_input:ServiceSectionInput|ServiceInput) -> Service:
    service = None
    if _input.service_pk:
        try:
            service = Service.objects.get(pk=_input.service_pk)
        except Service.DoesNotExist as e:
            raise GraphQLError("Service not found by pk.") from e
    elif _input.service_title:
        try:
            service = Service.objects.get(title=_input.service_title)
        except Service.DoesNotExist as e:
            raise GraphQLError("Service not found by title.") from e
    else:
        raise GraphQLError("Either service_pk or service_title must be provided.")
    return service


def find_service_section(_input:ServiceSectionInput) -> ServiceSection:
    service = find_service(_input)
    try:
        service_section = ServiceSection.objects.get(service=service, order=_input.old_order)
    except ServiceSection.DoesNotExist as e:
        raise GraphQLError("Service section not found.")  from e
    return service_section


def validate_section_input(_input:ServiceSectionInput) -> ServiceSectionInput:
    filled_fields = [
        _input.subtitle, _input.content,
        _input.content, _input.youtube_url, 
        _input.image, _input.add,
        _input.characteristics
    ]
    non_empty_fields = [field for field in filled_fields if field is not None]
    if len(non_empty_fields) != 1:
        raise ValueError('Only one of subtitle, content, youtube_url, or image must be filled.')
    return _input


def null_section(service_section:ServiceSection) -> ServiceSection:
    service_section.subtitle = None
    service_section.content = None
    service_section.youtube_url = None
    service_section.image = None
    service_section.add = None
    service_section.characteristics = None
    return service_section

def save_section(_input:ServiceSectionInput, section:ServiceSection=None, service:Service=None) -> ServiceSection:
    if service:
        section = ServiceSection(
            service=service,
            order=_input.new_order,
            subtitle=_input.subtitle,
            content=_input.content,
            youtube_url=_input.youtube_url,
            image=_input.image,
            add=_input.add,
            characteristics=_input.characteristics
        )
        section.save()
        return section
    if _input.new_order is not None:
        section.order = _input.order
    if _input.subtitle is not None:
        section.subtitle = _input.subtitle
    if _input.content is not None:
        section.content = _input.content
    if _input.youtube_url is not None:
        section.youtube_url = _input.youtube_url
    if _input.image is not None:
        section.image = _input.image
    if _input.add is not None:
        section.add = _input.add
    if _input.characteristics is not None:
        section.characteristics = _input.characteristics
    section.save()
    return section


def save_service(_input:ServiceInput, service:Service=None, category:ServiceCategory=None,\
    subcategory:ServiceSubCategory=None) -> Service:
    if service is None:
        service = Service(
            title=_input.new_service_title,
            preview_text=_input.preview_text,
            preview_video_url=_input.preview_video_url,
            preview_image=_input.preview_image,
            category=category,
            subcategory=subcategory,
            price=_input.price
        )
        service.save()
        return service
    if title:=_input.new_service_title is not None:
        service.title = title
    if preview_text:=_input.preview_text is not None:
        service.preview_text = preview_text
    if preview_video_url:=_input.preview_video_url is not None:
        service.preview_image = None
        service.preview_video_url = preview_video_url
    if preview_image:=_input.preview_image is not None:
        service.preview_video_url = None
        service.preview_image = preview_image
    if category:=_input.category is not None:
        service.category = category
    if subcategory:=_input.subcategory is not None:
        service.subcategory = subcategory
    if price:=_input.price is not None:
        service.price = price
    service.save()
    return service


def validate_input_cat_subcat(_input:ServiceInput, flag:bool=None) -> tuple[ServiceCategory, ServiceSubCategory]:
    if flag is None:
        if not _input.category:
            raise GraphQLError("Category must be provided.")
        if not _input.subcategory:
            raise GraphQLError("Subcategory must be provided.")
    try:
        if _input.category is None:
            category = None
        else:
            category = ServiceCategory.objects.get(name=_input.category)
    except ServiceCategory.DoesNotExist as e:
        raise GraphQLError("Category not found.") from e
    try:
        if _input.subcategory is None:
            subcategory = None
        else:
            subcategory = ServiceSubCategory.objects.get(name=_input.subcategory)
    except ServiceSubCategory.DoesNotExist as e:
        raise GraphQLError("Subcategory not found.") from e
    return category, subcategory


def add_tags(_input:ServiceInput, service:Service) -> Service:
    if _input.tags:
        for tag_name in _input.tags:
            tag, created = ServiceTags.objects.get_or_create(name=tag_name)
            service.tags.add(tag)
    service.save()
    return service


def remove_tags(_input: ServiceInput, service: Service) -> Service:
    if _input.tags_to_del:
        for tag_name in _input.tags_to_del:
            try:
                tag = ServiceTags.objects.get(name=tag_name)
                service.tags.remove(tag)
            except ServiceTags.DoesNotExist:
                continue
    service.save()
    return service

def get_category(_input:ServiceSubCategoryInput) -> ServiceCategory:
    if _input.category_pk:
        try:
            return ServiceCategory.objects.get(pk=_input.category_pk)
        except ServiceCategory.DoesNotExist as e:
            raise GraphQLError("Category not found by ID.") from e
    elif _input.category_name:
        try:
            return ServiceCategory.objects.get(name=_input.category_name)
        except ServiceCategory.DoesNotExist as e:
            raise GraphQLError("Category not found by name.") from e
    else:
        raise GraphQLError(
            "Either category ID or category \
            name must be provided."
        )


def get_subcategory(_input:ServiceSubCategoryInput) -> ServiceSubCategory:
    category = get_category(_input)
    try:
        if _input.pk:
            return ServiceSubCategory.objects.get(pk=_input.pk, category=category)
    except ServiceSubCategory.DoesNotExist as e:
        raise GraphQLError("SubCategory not found in the specified category") from e
