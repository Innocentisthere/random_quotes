from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("top_10", views.top_10_quotes, name="top_10"),
    path("add/", views.add_quote, name="add_quote"),
    path("vote/<int:quote_id>/<str:vote_type>/", views.vote_quote, name="vote_quote"),
]