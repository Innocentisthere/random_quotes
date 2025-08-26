import random
from django.shortcuts import render, redirect
from django.db.models import F
from .forms import QuoteForm
from .models import Quote


def index(request):
    quotes = Quote.objects.all()
    if not quotes.exists():
        return render(request, "quotes_app/no_quotes.html")

    # Выбор случайной цитаты с учетом веса
    weighted_quotes = []
    for q in quotes:
        weighted_quotes.extend([q.id] * q.weight)
    chosen_id = random.choice(weighted_quotes)
    quote = Quote.objects.get(id=chosen_id)

    # Увеличить счётчик просмотров
    quote.views = F("views") + 1
    quote.save(update_fields=["views"])
    quote.refresh_from_db()

    return render(request, "quotes_app/index.html", {"quote": quote})


def like_quote(request, quote_id):
    if request.session.get("liked_quote_id") == quote_id:
        return redirect("index")
    Quote.objects.filter(pk=quote_id).update(likes=F("likes") + 1)
    request.session["liked_quote_id"] = quote_id
    return redirect("index")

def dislike_quote(request, quote_id):
    if request.session.get("liked_quote_id") == quote_id:
        return redirect("index")
    Quote.objects.filter(pk=quote_id).update(dislikes=F("dislikes") + 1)
    request.session["liked_quote_id"] = quote_id
    return redirect("index")


def top_10_quotes(request):
    top_quotes = Quote.objects.order_by("-likes")[:10]
    return render(request, "quotes_app/top_10.html", {"quotes": top_quotes})


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = QuoteForm()
    return render(request, "quotes_app/add_quote.html", {"form": form})




