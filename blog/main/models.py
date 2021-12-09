from django.db import models


from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'),
                      ('published', 'Published'))
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique_for_date='publish', db_index=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('single_url', kwargs={'slug': self.slug, 'pk': self.pk})

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse('category_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse('tag_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=10)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return f'Message by {self.first_name} {self.last_name}, email {self.email}'

