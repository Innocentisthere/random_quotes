from django.core.exceptions import ValidationError
from django.db import models

class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=100)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def clean(self):
        # ограничение: максимум 3 цитаты от одного источника
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= 3:
            raise ValidationError(f"Источник '{self.source}' уже имеет 3 цитаты.")

    def __str__(self):
        return f"{self.text[:50]}... ({self.source})"
