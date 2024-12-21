import graphene, graphql_jwt
from graphene_django.types import DjangoObjectType
from blog.models import BlogPost, BlogPostSection
from graphql import GraphQLError


class BlogPostSectionType(DjangoObjectType):
    class Meta:
        model = BlogPostSection


class CreateBlogPostSectionInput(graphene.InputObjectType):
    post_id = graphene.Int(required=True)
    order = graphene.Int(required=True)
    subtitle = graphene.String()
    content = graphene.String()
    youtube_url = graphene.String()
    image = graphene.String()


class UpdateBlogPostSectionInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    post_id = graphene.Int(required=True)
    order = graphene.Int()
    subtitle = graphene.String()
    content = graphene.String()
    youtube_url = graphene.String()
    image = graphene.String()


class CreateBlogPostSection(graphene.Mutation):
    class Arguments:
        input = CreateBlogPostSectionInput()

    blog_post_section = graphene.Field(lambda: BlogPostSectionType)

    def mutate(self, info, input:CreateBlogPostSectionInput):
        try:
            blog_post = BlogPost.objects.get(pk=input.post_id)
        except BlogPost.DoesNotExist as e:
            raise GraphQLError("Post not found.") from e
        blog_post_section = BlogPostSection(
            post=blog_post,
            order=input.order,
            subtitle=input.subtitle,
            content=input.content,
            youtube_url=input.youtube_url,
            image=input.image
        )
        blog_post_section.save()
        return CreateBlogPostSection(blog_post_section=blog_post_section)


class UpdateBlogPostSection(graphene.Mutation):
    class Arguments:
        input = UpdateBlogPostSectionInput()

    blog_post_section = graphene.Field(lambda: BlogPostSectionType)

    def mutate(self, info, input:UpdateBlogPostSectionInput):
        try:
            blog_post_section = BlogPostSection.objects.get(pk=input.id)
        except BlogPostSection.DoesNotExist as e:
            raise GraphQLError("Section not found.") from e
        if input.post_id:
            try:
                blog_post = BlogPost.objects.get(pk=input.post_id)
            except BlogPost.DoesNotExist as e:
                raise GraphQLError("Post not found.") from e
            blog_post_section.post = blog_post
        if input.order:
            blog_post_section.order = input.order
        if input.subtitle:
            blog_post_section.subtitle = input.subtitle
        if input.content:
            blog_post_section.content = input.content
        if input.youtube_url:
            blog_post_section.youtube_url = input.youtube_url
        if input.image:
            blog_post_section.image = input.image
        blog_post_section.save()
        return UpdateBlogPostSection(blog_post_section=blog_post_section)


class BlogSectionMutation(graphene.ObjectType):
    create_blog_post_section = CreateBlogPostSection.Field()
    update_blog_post_section = UpdateBlogPostSection.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()