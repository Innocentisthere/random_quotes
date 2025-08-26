from django.db import models
from django.core.exceptions import ValidationError

class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=100)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)

    def clean(self):
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= 3:
            raise ValidationError({"source": f"Source «{self.source}» already have 3 quotes."})

    def likes_count(self):
        return self.votes.filter(value=1).count()

    def dislikes_count(self):
        return self.votes.filter(value=-1).count()

    def __str__(self):
        return f"{self.text[:50]}... ({self.source})"


class QuoteVote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    session_key = models.CharField(max_length=40)  # ключ сессии пользователя
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        unique_together = ('quote', 'session_key')  # один голос от одной сессии
