from django.urls import path
from . import views
from .feeds import LatestPostsFeed
from .views import AddPostAPI, EditPostAPI, RegisterUserAPI

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('add/', views.add_post, name='add_post'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name = 'post_feed'),
    path('search/', views.post_search, name='post_search'),

    path('api/posts/add/', AddPostAPI.as_view(), name='api_add_post'),
    path("api/register/", RegisterUserAPI.as_view(), name="api_register"),
    path("api/posts/<int:post_id>/edit/", EditPostAPI.as_view(), name="edit_post"),
    path("edit/<int:post_id>/", views.edit_post_page, name="edit_post_page"),


]

