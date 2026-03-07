from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def index(request):
    """The home page for the blog."""
    posts = Post.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)


def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


def edit_post(request, post_id):
    """Edit an existing post."""
    post = Post.objects.get(id=post_id)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)