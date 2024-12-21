import graphene
from blog.models import BlogPost, BlogPostSection

class Query(graphene.ObjectType):
    blog_post = graphene.Field(BlogPostType, id=graphene.Int())
    blog_posts = graphene.List(BlogPostType, ids=graphene.List(graphene.Int))
    blog_post_section = graphene.Field(BlogPostSectionType, id=graphene.Int(), post_id=graphene.Int())
    blog_post_sections = graphene.List(BlogPostSectionType, post_id=graphene.Int())

    def resolve_blog_post(self, info, id):
        try:
            return BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist:
            return None

    def resolve_blog_posts(self, info, ids=None):
        return BlogPost.objects.filter(pk__in=ids) if ids else BlogPost.objects.all()

    def resolve_blog_post_section(self, info, id, post_id):
        try:
            return BlogPostSection.objects.get(pk=id, post_id=post_id)
        except BlogPostSection.DoesNotExist:
            return None

    def resolve_blog_post_sections(self, info, post_id):
        return BlogPostSection.objects.filter(post_id=post_id)

schema = graphene.Schema(query=Query, mutation=Mutation)