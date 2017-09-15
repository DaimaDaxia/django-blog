from django.db import models
from django.urls import reverse
from markdown import Markdown
from django.utils.html import strip_tags
# User是一个自带的模型类，里面是用户的字段
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    views = models.IntegerField(default=0)
    # 摘要
    excerpt = models.CharField(max_length=256,blank=True)

    # 关系
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)

    author = models.ForeignKey(User)

    class Meta:
        ordering = ['-created_time', '-modified_time']

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = Markdown(extensions={
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            })
            self.excerpt = strip_tags(md.convert(self.body))[:32]
        super().save(*args, **kwargs)


