from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

def paginateObjects(request, objects, results):
    page = request.GET.get('page')
    paginator = Paginator(objects, results)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)
    leftIndex = (int(page) - 4)
    leftIndex = max(leftIndex, 1)
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custom_range = range(leftIndex, rightIndex)
    return custom_range, objects


def add_cache_control_headers(headers, path, url):
    if url.startswith('/static/'):
        headers['Cache-Control'] = f'max-age={settings.CLIENT_CACHE_MAX_AGE}, public'


def get_admin_profile_id():
    from django.contrib.auth.models import User
    admin_user = User.objects.filter(is_superuser=True).first()
    admin_profile = admin_user.profile if admin_user else None
    return admin_profile.id if admin_profile else None
