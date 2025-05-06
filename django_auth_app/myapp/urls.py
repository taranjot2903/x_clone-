from django.urls import path
from . import views

urlpatterns = [
    # Authentication Views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Core App Views
    path('', views.index_view, name='index'),
    path('explore/', views.explore_view, name='explore'),
    path('messages/', views.messages_view, name='messages'),
    path('settings/', views.settings_view, name='settings'),

    # Tweet Functionality
    path('post/', views.post_tweet, name='post_tweet'),
]

