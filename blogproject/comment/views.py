from django.shortcuts import redirect,render,get_object_or_404

from blog.models import Post

from .models import Comment
from .forms import CommentForm

def post_comment(request, post_pk):
    """
    获取要评论的文章
    :return:
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)



