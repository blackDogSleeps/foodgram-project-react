from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-author']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return (f'Пользователь: {self.user} '
                f'Автор: {self.author}')
