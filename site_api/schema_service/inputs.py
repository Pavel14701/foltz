import graphene

class ServiceSectionInput(graphene.InputObjectType):
    service_pk = graphene.ID()  # Для поиска по pk
    service_title = graphene.String()  # Для поиска по заголовку
    old_order = graphene.Int()
    new_order = graphene.Int()
    subtitle = graphene.String()
    content = graphene.String()
    youtube_url = graphene.String()
    image = graphene.String() # URL или base64?
    add = graphene.JSONString() 
    characteristics = graphene.JSONString()


class ServiceInput(graphene.InputObjectType):
    service_pk = graphene.ID()  # Для поиска по pk
    service_title = graphene.String()  # Для поиска по заголовку
    new_service_title = graphene.String()
    category = graphene.String(required=True)
    subcategory = graphene.String(required=True)
    preview_text = graphene.String(required=True) 
    preview_video_url = graphene.String() 
    preview_image = graphene.String() # base64 или url ?
    price = graphene.Int()
    tags = graphene.List(graphene.String)
    tags_to_del = graphene.List(graphene.String)


class ServiceCategoryInput(graphene.InputObjectType):
    pk = graphene.ID()
    name = graphene.String()
    new_name = graphene.String()


class ServiceSubCategoryInput(graphene.InputObjectType):
    pk = graphene.ID()
    name = graphene.String()
    new_name = graphene.String()
    category_pk = graphene.ID()
    category_name = graphene.String()