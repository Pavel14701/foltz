import graphene, graphql_jwt
from django.db.models import Model
from graphene_django.types import DjangoObjectType
from blog.models import BlogPost
from graphql import GraphQLError


def save_obj(model_type:Model, command:dict[str, str], input:graphene.InputObjectType, exc_info:str=None) -> None:
    if command.get('method') == 'update':
        try:
            _object = model_type.objects.get(pk=input.id)
        except model_type.DoesNotExist as e:
            raise GraphQLError(exc_info or f" {model_type.__name__} not found.") from e
    for _field in command.get('fields'):
        match _field:
            case 'title':
                _object.title = _field
            case 'preview_text':
                _object.preview_text = _field
            case 'preview_video_url': 
                _object.preview_video_url = _field
            case 'preview_image' :
                _object.preview_image = _field
            case _:
                raise GraphQLError(f"Field {_field} not founded in model {model_type.__name__}")
    _object.save()
    return _object


class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost


class CreateBlogPostInput(graphene.InputObjectType): 
    title = graphene.String(required=True) 
    preview_text = graphene.String(required=True) 
    preview_video_url = graphene.String() 
    preview_image = graphene.String()


class CreateBlogPost(graphene.Mutation): 
    class Arguments: 
        input = CreateBlogPostInput(required=True) 
        blog_post = graphene.Field(BlogPostType) 
        
    def mutate(self, info, input:CreateBlogPostInput): 
        blog_post = BlogPost(
            title=input.title,
            preview_text=input.preview_text,
            preview_video_url=input.preview_video_url,
            preview_image=input.preview_image 
        ) 
        blog_post.save() 
        return CreateBlogPost(blog_post=blog_post)


class CreateMultipleBlogPosts(graphene.Mutation):
    class Arguments:
        posts = graphene.List(CreateBlogPostInput)

    blog_posts = graphene.List(lambda: BlogPostType)

    def mutate(self, info, posts:list[CreateBlogPostInput]):
        blog_posts = []
        for post_data in posts:
            blog_post = BlogPost(title=post_data.title)
            blog_post.save()
            blog_posts.append(blog_post)
        return CreateMultipleBlogPosts(blog_posts=blog_posts)


class UpdateBlogPostInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    title = graphene.String() 
    preview_text = graphene.String() 
    preview_video_url = graphene.String() 
    preview_image = graphene.String()


class UpdateBlogPost(graphene.Mutation):
    class Arguments:
        input = UpdateBlogPostInput()

    blog_post = graphene.Field(lambda: BlogPostType)

    def mutate(self, info, input:UpdateBlogPostInput) -> 'UpdateBlogPost':
        command = {
            'method': 'update',
            'fields': [
                'title', 'preview_text',
                'preview_video_url', 'preview_image'
            ]
        }
        blog_post = save_obj(BlogPost, command, input, exc_info="Post not found.")
        return UpdateBlogPost(blog_post=blog_post)


class UpdateMultipleBlogPosts(graphene.Mutation):
    class Arguments:
        posts = graphene.List(UpdateBlogPostInput)

    blog_posts = graphene.List(lambda: BlogPostType)

    def mutate(self, info, posts):
        updated_posts = []
        command = {
            'method': 'update',
            'fields': [
                'title', 'preview_text',
                'preview_video_url', 'preview_image'
            ]
        }
        for post_data in posts:
            blog_post = save_obj(BlogPost, command, post_data, exc_info="Post not found.")
            updated_posts.append(blog_post)
        return UpdateMultipleBlogPosts(blog_posts=updated_posts)





class DeleteBlogPost(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            blog_post = BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist as e:
            raise GraphQLError("Post not found.") from e
        blog_post.delete()
        return DeleteBlogPost(ok=True)



class DeleteMultipleBlogPosts(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.Int)

    ok = graphene.Boolean()

    def mutate(self, info, ids):
        BlogPost.objects.filter(pk__in=ids).delete()
        return DeleteMultipleBlogPosts(ok=True)





class BlogPostMutation(graphene.ObjectType):
    create_blog_post = CreateBlogPost.Field()
    create_multiple_blog_posts = CreateMultipleBlogPosts.Field()
    update_blog_post = UpdateBlogPost.Field()
    update_multiple_blog_posts = UpdateMultipleBlogPosts.Field()
    delete_blog_post = DeleteBlogPost.Field()
    delete_multiple_blog_posts = DeleteMultipleBlogPosts.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(graphene.ObjectType):
    blog_post = graphene.Field(BlogPostType, id=graphene.Int())
    blog_posts = graphene.List(BlogPostType)

    def resolve_blog_post(self, info, id):
        try:
            return BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist:
            return None

    def resolve_blog_posts(self, info):
        return BlogPost.objects.all()
