from django.db import models
from django.utils.text import slugify
from django.conf import settings
from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Kategoriyalar"
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Article(models.Model):
    STATUS = (('draft','qoralama'), ('published','Nashr etilgan'))
    title= models.CharField(max_length=250)
    slug= models.SlugField(unique=True, blank=True)
    cover = models.ImageField(upload_to='articles/', blank=True, null=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles' )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs) :
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

def __str__ (self):
    return self. title
class Meta:
    ordering = ['-created_at']
    verbose_name_plural = "YangiLikLar"
































class ContactMessage(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        subject = models.CharField(max_length=200)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.name} - {self.subject}"

        class Meta:
            ordering = ['-created_at']


