from django.shortcuts import render,get_object_or_404
from markdown import markdown

from .models import Post,Category
from comment.models import Comment
from comment.forms import CommentForm


def index(request):
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})
    # return HttpResponse('<h1>hello world</h1>')

def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    print("*******************", comment_list)
    context ={
        'post': post,
        'form': form,
        'comment_list': comment_list,
    }
    post.increaseViews()
    return render(request,'blog/detail.html',context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request,'blog/index.html',context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
