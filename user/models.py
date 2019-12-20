from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return '<Profile %s for %s>' % (self.nickname, self.user.username)

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        return Profile.objects.get(user=self).nickname
    else:
        return self.username

User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username