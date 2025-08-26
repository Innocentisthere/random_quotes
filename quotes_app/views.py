import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Count, Q
from .forms import QuoteForm
from .models import Quote, QuoteVote


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

    # Увеличиваем просмотры
    quote.views = F("views") + 1
    quote.save(update_fields=["views"])
    quote.refresh_from_db()

    # Создаём сессию если её ещё нет
    if not request.session.session_key:
        request.session.create()

    # Получаем голос пользователя для этой цитаты
    user_vote = quote.votes.filter(session_key=request.session.session_key).first()

    return render(request, "quotes_app/index.html", {
        "quote": quote,
        "user_vote": user_vote,
    })


def vote_quote(request, quote_id, vote_type):
    quote = get_object_or_404(Quote, pk=quote_id)

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    current_vote = QuoteVote.objects.filter(quote=quote, session_key=session_key).first()

    # логика как раньше
    if vote_type == "like":
        if current_vote and current_vote.value == 1:
            current_vote.delete()
        else:
            QuoteVote.objects.update_or_create(
                quote=quote,
                session_key=session_key,
                defaults={"value": 1}
            )

    elif vote_type == "dislike":
        if current_vote and current_vote.value == -1:
            current_vote.delete()
        else:
            QuoteVote.objects.update_or_create(
                quote=quote,
                session_key=session_key,
                defaults={"value": -1}
            )

    # обновляем объект с новыми данными
    quote.refresh_from_db()

    return JsonResponse({
        "likes": quote.likes_count(),
        "dislikes": quote.dislikes_count(),
        "user_vote": QuoteVote.objects.filter(quote=quote, session_key=session_key).first().value if QuoteVote.objects.filter(quote=quote, session_key=session_key).exists() else 0
    })


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


from django.db.models import Count, Q, Value
from django.db.models.functions import Coalesce

def top_10_quotes(request):
    top_quotes = (
        Quote.objects
        .annotate(like_count=Coalesce(Count("votes", filter=Q(votes__value=1)), Value(0)))
        .annotate(dislike_count=Coalesce(Count("votes", filter=Q(votes__value=-1)), Value(0)))
        .order_by("-like_count")[:10]
    )
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




