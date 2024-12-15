from django.urls import path, include
from blog import views
from rest_framework.routers import DefaultRouter
from blog.api.views import PostViewSet, SectionSearchView

app_name = "blog"

urlpatterns = [
    # Для получения списка постов
    path('api/posts/',
        PostViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='post-list'),
    # Для создания нового поста
    path('api/posts/create/',
        PostViewSet.as_view({'post': 'create'}), 
        name='post-create'),
    # Для получения информации о конкретном посте
    path('api/posts/<int:pk>/',
        PostViewSet.as_view({'get': 'retrieve'}),
        name='post-detail'),
    # Для обновления поста
    path('api/posts/<int:pk>/update/',
        PostViewSet.as_view({'put': 'update'}),
        name='post-update'),
    # Для частичного обновления поста
    path('api/posts/<int:pk>/partial_update/',
        PostViewSet.as_view({'patch': 'partial_update'}),
        name='post-partial-update'),
    # Для удаления поста
    path('api/posts/<int:pk>/delete/',
        PostViewSet.as_view({'delete': 'destroy'}),
        name='post-delete'),
    # Для получения всех секций поста
    path('api/posts/<int:pk>/sections/',
        PostViewSet.as_view({'get': 'get_post_sections'}),
        name='post-sections'),
    # Для получения информации о секции поста
    path('api/posts/<int:post_id>/sections/<int:section_id>/', 
        SectionSearchView.as_view({'get': 'retrieve'}), 
        name='post-section-detail'),
    # Для обновления секции поста
    path('api/posts/<int:post_id>/sections/<int:section_id>/update/', 
        SectionSearchView.as_view({'put': 'update'}), 
        name='post-section-update'),
    # Для частичного обновления секции поста
    path('api/posts/<int:post_id>/sections/<int:section_id>/partial_update/', 
        SectionSearchView.as_view({'patch': 'partial_update'}), 
        name='post-section-partial-update'),
    # Для удаления секции поста
    path('api/posts/<int:post_id>/sections/<int:section_id>/delete/', 
        SectionSearchView.as_view({'delete': 'destroy'}), 
        name='post-section-delete'),
    # Для перемещения секции поста
    path('api/posts/<int:post_id>/sections/<int:section_id>/move/', 
        SectionSearchView.as_view({'post': 'move_post_section'}), 
        name='post-section-move'),
    # Для создания новой секции поста
    path('api/posts/<int:post_id>/sections/create/', 
        SectionSearchView.as_view({'post': 'create'}), 
        name='post-section-create'),
    # Отображение блога
    path('blog/', views.blog, name="blog")
]