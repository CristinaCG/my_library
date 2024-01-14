from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Film

class FilmList(ListView):
    model = Film
    template_name = 'film_list.html'
    context_object_name = 'Films'

class FilmDetail(DetailView):
    model = Film
    template_name = 'film_detail.html'
    context_object_name = 'Film'
