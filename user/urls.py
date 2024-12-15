from django.urls import path
from user.api.views import MessageListView
from . import views

urlpatterns = [
    path('api/messages/', MessageListView.as_view(), name='message-list'),
    #path('', views.landing, name='landing'),
    #path('landing/', views.landing_login, name='landingLogin'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),   
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit-account'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('create-message/<str:username>/', views.create_message, name='create-message'),
]
