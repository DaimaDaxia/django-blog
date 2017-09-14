from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView
from markdown import markdown

from .models import Post,Category
from comment.models import Comment
from comment.forms import CommentForm

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, args, kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object()
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context

class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get("year"),
                                             created_time__month=self.kwargs.get("month"))

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)



