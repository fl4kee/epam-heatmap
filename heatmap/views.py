from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render


def show_heatmap(request: WSGIRequest) -> HttpResponse:
    return render(request, "heatmap/heatmap.html")


def show_default(request: WSGIRequest) -> HttpResponse:
    return redirect("/spb")
