import graphene, graphql_jwt
from blog.models import BlogPost, BlogPostSection
from site_api.schema_blog.post_shema import BlogPostType, BlogPostMutation
from site_api.schema_blog.section_schema import BlogPostSectionType, BlogSectionMutation
from site_api.schema_service.service import ServiceType, ServiceMutation

class Mutation(ServiceMutation): 
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

