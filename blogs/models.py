from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.name

class BlogModel(models.Model):
    title = models.CharField(max_length=50, null = False, blank=False)
    description = models.TextField('body')
    image = models.ImageField(upload_to="blogImages/", null=True, blank=True)
    tags = models.ManyToManyField(Tags)
    
    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return self.title
    
class Comment(models.Model):
        post = models.ForeignKey(BlogModel,on_delete=models.CASCADE,related_name='comments', blank=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
        body = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        # active = models.BooleanField(default=False)

        def __str__(self):
            return '%s - %s' % (self.post.title, self.user)
        
        @property
        def number_of_comments(self):
            return Comment.objects.filter(post=self).count()
    
