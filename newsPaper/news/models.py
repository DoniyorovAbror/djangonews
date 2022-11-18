from django.contrib.auth.models import User
from django.db import models

from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    
    def update_rating(self):
        postRate = Post.objects.filter(author=self.pk).values_list('rating', flat=True).aggregate(Sum('rating'))
        commentRate = Comment.objects.filter(commentUser__author=self.pk).values_list('rating', flat=True).aggregate(Sum('rating'))
        cpRate = Comment.objects.filter(commentThrough__in=Post.objects.filter(author=self.pk)).values_list('rating', flat=True).aggregate(Sum('rating'))
        self.ratingAuthor = postRate['rating__sum'] * 3 + commentRate['rating__sum'] + cpRate['rating__sum']
        self.save()
        
    def __str__(self):
        return f'{self.authorUser}'
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    sport = 'SP'
    politics = 'PO'
    education = 'ED'
    cinema = 'CI'
    information = 'IT'
    CATS = [(sport, 'Спорт'),
            (politics, 'Политика'),
            (education, 'Образование'),
            (cinema, 'Кино'),
            (information, 'Сфера IT')
            ]
    name = models.CharField(max_length = 2, choices = CATS, default = sport, unique = True)
    subscribers = models.ManyToManyField(User)
    
    def __str__(self):
        return f'{self.get_name_display()}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
    
    def preview(self):
        return self.text[0:128] + '...'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'{self.id}'
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()
