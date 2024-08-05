from django.contrib.auth.models import AbstractUser
from django.db import models
    
    
class User(AbstractUser):
    followers = models.ManyToManyField('Follower', default=None, related_name='followers')
    followings = models.ManyToManyField('Following', default=None, related_name='followings') 
    def __str__(self):
        return f"Profile: {self.username}, followers: {self.followers.count()}, following: {self.followings.count()}"
    

class Post(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    liked = models.ManyToManyField(User, default=None, related_name="liked")
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Post id: {self.id}, username: {self.username}, likes: {self.likes}"
    
    def num_likes(self):
        return f"likes: {self.liked.all().count()}"
    
   
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} likes {self.post}"
    
    
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

    

