from django.shortcuts import render
from common.utils import paginateObjects

# Create your views here.
def blog(request):
    profile = request.user.profile
    posts = profile.post_set.all()
    tags, categories = get_tags_categories(posts)
    custom_range, posts = paginateObjects(request, posts, 3)
    context = {'profile': profile, 'posts': posts, 
    'custom_range': custom_range, 'tags': tags, 
    'categories': categories}
    return render(request, 'blog/post_{title}.html', context)

def get_tags_categories(posts):
    categories = set()
    tags = set()
    for post in posts:
        categories.add(post.category)
        for tag in post.tags.all():
            tags.add(tag)
    return tags, categories