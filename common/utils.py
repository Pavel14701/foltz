from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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

