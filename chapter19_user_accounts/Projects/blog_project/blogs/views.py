from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Blog, Post
from .forms import PostForm


def index(request):
    """The home page for the blog."""
    posts = Post.objects.order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)


def check_post_owner(request, post):
    """Raise 404 if the current user does not own the post's blog."""
    if post.blog.owner != request.user:
        raise Http404


@login_required
def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        form = PostForm()
        # Mostrar solo los blogs del usuario logueado
        form.fields['blog'].queryset = Blog.objects.filter(owner=request.user)
    else:
        form = PostForm(data=request.POST)
        form.fields['blog'].queryset = Blog.objects.filter(owner=request.user)

        if form.is_valid():
            selected_blog = form.cleaned_data['blog']

            # Seguridad extra: asegurar que el blog elegido es del usuario actual
            if selected_blog.owner != request.user:
                raise Http404

            form.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    post = get_object_or_404(Post, id=post_id)
    check_post_owner(request, post)

    if request.method != 'POST':
        form = PostForm(instance=post)
        form.fields['blog'].queryset = Blog.objects.filter(owner=request.user)
    else:
        form = PostForm(instance=post, data=request.POST)
        form.fields['blog'].queryset = Blog.objects.filter(owner=request.user)

        if form.is_valid():
            edited_blog = form.cleaned_data['blog']

            # Seguridad extra: asegurar que el blog seleccionado también es del usuario
            if edited_blog.owner != request.user:
                raise Http404

            form.save()
            return redirect('blogs:index')

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)