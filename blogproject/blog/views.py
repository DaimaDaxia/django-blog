from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView
from markdown import markdown

from .models import Post, Category, Tag
from comment.models import Comment
from comment.forms import CommentForm

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        more_pages = 2
        first = False
        left_has_more = False
        left = []
        page_number = page.number
        right = []
        right_has_more = False
        last = False
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number+more_pages]
            if right[-1]<total_pages-1:
                right_has_more = True
            if right[-1]<total_pages:
                last = True
        elif page_number == total_pages:
            temp = page_number-more_pages-1
            left = page_range[(temp if temp > 0 else 0):page_number-1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            temp = page_number-more_pages-1
            left = page_range[(temp if temp > 0 else 0):page_number-1]
            right = page_range[page_number:page_number + more_pages]
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1]<total_pages:
                last=True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        context.update(self.pagination_data(paginator,page,is_paginated))
        return context

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

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_pk'))
        return super().get_queryset().filter(tags=tag)


