from django.urls import path
from blog import views
from blog.api.views import BlogViewSet, BlogSectionSearchView

app_name = "blog"

urlpatterns = [
    # Для получения списка постов
    path('api/list/',
        BlogViewSet.as_view({'get': 'list'}),
        name='post-list'),
    # Для создания нового поста
    path('api/create/',
        BlogViewSet.as_view({'post': 'create'}), 
        name='post-create'),
    # Для получения информации о конкретном посте
    path('api/<int:pk>/',
        BlogViewSet.as_view({'get': 'retrieve'}),
        name='post-detail'),
    # Для обновления поста
    path('api/<int:pk>/update/',
        BlogViewSet.as_view({'put': 'update'}),
        name='post-update'),
    # Для частичного обновления поста
    path('api/<int:pk>/partial_update/',
        BlogViewSet.as_view({'patch': 'partial_update'}),
        name='post-partial-update'),
    # Для удаления поста
    path('api/<int:pk>/delete/',
        BlogViewSet.as_view({'delete': 'destroy'}),
        name='post-delete'),
    # Для получения всех секций поста
    path('api/<int:pk>/sections/',
        BlogViewSet.as_view({'get': 'get_post_sections'}),
        name='post-sections'),
    # Для получения информации о секции поста
    path('api/<int:post_id>/sections/<int:section_id>/', 
        BlogSectionSearchView.as_view({'get': 'retrieve'}), 
        name='post-section-detail'),
    # Для обновления секции поста
    path('api/<int:post_id>/sections/<int:section_id>/update/', 
        BlogSectionSearchView.as_view({'put': 'update'}), 
        name='post-section-update'),
    # Для частичного обновления секции поста
    path('api/<int:post_id>/sections/<int:section_id>/partial_update/', 
        BlogSectionSearchView.as_view({'patch': 'partial_update'}), 
        name='post-section-partial-update'),
    # Для удаления секции поста
    path('api/<int:post_id>/sections/<int:section_id>/delete/', 
        BlogSectionSearchView.as_view({'delete': 'destroy'}), 
        name='post-section-delete'),
    # Для перемещения секции поста
    path('api/<int:post_id>/sections/<int:section_id>/move/', 
        BlogSectionSearchView.as_view({'post': 'move_post_section'}), 
        name='post-section-move'),
    # Для создания новой секции поста
    path('api/<int:post_id>/sections/create/', 
        BlogSectionSearchView.as_view({'post': 'create'}), 
        name='post-section-create'),
    # Отображение блога
    path('', views.blog, name="blog")
]