from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    STATUS = (
        ('public', 'public'),
        ('private', 'private'),
    )
    name = models.CharField(max_length=250)
    user = models.OneToOneField(User,  related_name="accuser", on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="follower", through="Follow")
    status = models.CharField(max_length=10, choices=STATUS, default='public')
    profpic = models.ImageField(upload_to='upload/', blank=True, null=True)
    bio = models.TextField(default="")

    def __str__(self):
        return f"{self.user}"


class Follow(models.Model):
    user = models.ForeignKey(User, related_name="fuser", on_delete=models.CASCADE)
    profile = models.ForeignKey(Account, related_name="fprofile", on_delete=models.CASCADE)
    verify = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} follows {self.profile.user.username}"

    def save(self, *args, **kwargs):
        if self.profile.user.id == self.user.id:
            raise Exception("shab bekheir")

        return super().save(*args, **kwargs)


class Post(models.Model):
    account = models.ForeignKey(Account, related_name="accountpost", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    likes = models.ManyToManyField(User, related_name="postlikes", through="Likes")

    def __str__(self):
        return f'{self.title}-{self.id}-{self.account} account'


class Likes(models.Model):
    user = models.ForeignKey(User, related_name="luser", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="lpost", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} like kard {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comentpost = models.ForeignKey(Post, related_name="commentpost", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'{self.user}-{self.description}'

# def model_image_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#     return f'{instance.__class__.__name__}/{instance.product.id}/{filename}'
