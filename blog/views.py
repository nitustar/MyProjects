from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from .models import Post
from .serializers import PostSerializer, EditPostSerializer, RegisterUserSerializer
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm
from taggit.models import Tag
from django.contrib.postgres.search import (SearchVector, SearchQuery, SearchRank)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.text import slugify
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q


# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 4
#     template_name = 'blog/post/list.html'



@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, 'blog/post/add_blog.html', {'form': form})


def post_list(request, tag_slug=None):
    status_filter = request.GET.get("status")
    # post_list = Post.objects.all()
    if request.user.is_authenticated:
        post_list = Post.objects.filter(
            Q(status=Post.Status.PUBLISHED) |
            Q(author=request.user)
        )
    else:
        post_list = Post.objects.filter(status=Post.Status.PUBLISHED)

    if status_filter == "published":
        post_list = post_list.filter(status=Post.Status.PUBLISHED)

    elif status_filter == "draft":
        post_list = post_list.filter(
            status=Post.Status.DRAFT,
            author=request.user
        )
        
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 4 posts per page
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', 
                  {'posts':posts, 'tag':tag, "status_filter": status_filter})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # 🚨 Draft protection
    if post.status == Post.Status.DRAFT:
        if not request.user.is_authenticated:
            return HttpResponseForbidden("This post is in draft")

        if request.user != post.author:
            return HttpResponseForbidden("This post is in draft")

    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, "blog/post/detail.html", {
        "posts": post,
        "comments": comments,
        "form": form
    })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post, id = post_id,
        status = Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        # Form fields passed validation
        if form.is_valid():
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']})" f" recommends you read {post.title}")
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']} \'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, 'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data = request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )


class AddPostAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                slug=slugify(serializer.validated_data['title'])
            )
            return Response({"message": "Post created successfully"}, status=201)

        return Response(serializer.errors, status=400)


class RegisterUserAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)

class EditPostAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # 🔐 Only author can update
        if post.author != request.user:
            return Response(
                {"detail": "You are not allowed to edit this post"},
                status=403
            )

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True   # ✅ THIS IS CRITICAL
        )

        if serializer.is_valid():
            updated_post = serializer.save()

            # Optional: update slug if title changed
            if "title" in request.data:
                updated_post.slug = slugify(updated_post.title)
                updated_post.save()

            return Response({"message": "Post updated successfully"}, status=200)

        return Response(serializer.errors, status=400)

@login_required
def edit_post_page(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 🚨 Only author can edit
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post")

    return render(request, "blog/post/edit_blog.html", {"post": post})
