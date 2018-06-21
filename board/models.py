from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('제목을 3글자 이상 입력해주세요.')

def min_length_10_validator(value):
    if len(value) < 10:
        raise forms.ValidationError('내용을 10글자 이상 입력해주세요.')

class Post(models.Model):
    title = models.CharField(max_length=30, validators=[min_length_3_validator])
    text = models.TextField(validators=[min_length_10_validator])
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    regdate = models.DateTimeField(auto_created=True, auto_now_add=True)

    def generate(self):
        self.save()

    def __str__(self):
        return '%s by %s'%(self.title, self.author)


class Comment(models.Model):
    post = models.ForeignKey('board.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text