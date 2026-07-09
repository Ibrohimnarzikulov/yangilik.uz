from django.db import models
from django.conf import settings
from news.models import Article


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    perent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='reply')
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.author.username} -> {self.article.title}"


class Like(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('article', 'user')
