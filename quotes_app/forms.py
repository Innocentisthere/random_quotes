from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Введите цитату"}),
            "source": forms.TextInput(),
         }

        labels = {
            "text": "Текст цитаты",
            "source": "Источник(автор)",
            "weight": "Вес цитаты"
        }
