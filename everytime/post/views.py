from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import *
from django.contrib.auth.decorators import login_required

def list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    return render(request, 'post/list.html', {'posts' : posts, 'categories' : categories})

def category(request, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-id')
    return render(request, 'post/category.html', {'posts' : posts, 'category' : category, 'categories' : categories})

@login_required
def create(request, slug):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        anonymity = 'anonymity' in request.POST
        category = Category.objects.get(slug=slug)
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        post = Post.objects.create(
            title = title,
            content = content,
            anonymity = anonymity,
            author = request.user,
            image = image,
            video = video
        )
        post.category.add(category)

        return redirect('post:category', slug)
    return render(request, 'post/list.html', {'category' : category})

def detail(request, id):
    post = get_object_or_404(Post, id = id)
    return render(request, 'post/detail.html', {'post' : post})

@login_required
def update(request, id):
    post = get_object_or_404(Post, id = id)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if image:
            post.image.delete()
            post.image = image
        if video:
            post.video.delete()
            post.video = video

        post.save()
        return redirect('post:detail', id)
    return render(request, 'post/update.html', {'post' : post})

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    return redirect('post:list')

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    anonymity = 'anonymity' in request.POST
    
    if request.method == "POST":
        Comment.objects.create(
            content = request.POST.get('content'),
            anonymity = anonymity,
            author = request.user,
            post = post
        )
        return redirect('post:detail', post_id)
    
@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id = post_id)
    comment = get_object_or_404(Comment, id = comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("댓글 작성자만 삭제 가능합니다.")
    
    comment.delete()
    return redirect('post:detail', post_id)

def add_like(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.like.add(request.user)
    return redirect('post:detail', post_id)

def remove_like(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.like.remove(request.user)
    return redirect('post:detail', post_id)

def add_scrap(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.scrap.add(request.user)
    return redirect('post:detail', post_id)

def remove_scrap(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.scrap.remove(request.user)
    return redirect('post:detail', post_id)