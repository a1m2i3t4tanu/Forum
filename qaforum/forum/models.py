from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_image = models.ImageField(upload_to='quest_pics', blank=True, null=True)
    question_file = models.FileField(upload_to='file_pics', blank=True, null=True)

    class Meta:
        ordering = ('-date_posted',)


    def __str__(self):
        return self.title

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    comment_image = models.ImageField(blank=True, upload_to='comment_pics', null=True)
    comment_file = models.FileField(blank=True, upload_to='comment_files', null=True)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text
