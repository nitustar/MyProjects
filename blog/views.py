from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Post
# Create your views here.

def post_list(requests):
    posts = Post.objects.all()
    return render(requests, 'blog/post/list.html', {'posts':posts})

def post_details(requests, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(requests, 'blog/post/detail.html', {'posts':post})