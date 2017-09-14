from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    url = models.URLField()

    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

