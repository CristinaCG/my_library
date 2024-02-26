from django.db import models

# Create your models here.
class Genre(models.Model):
    """ Modelo que representa el género literario de un libro"""
    name = models.CharField(max_length=255, help_text='Enter a book genre (e.g. Science Fiction, Poetry, Fantasy etc.)')

    def __str__(self):
        return self.name

class Language(models.Model):
    """ Modelo que representa el idioma de un libro"""
    name = models.CharField(max_length=255, help_text='Enter the book\'s language (e.g. English, French, Spanish etc.)')

    def __str__(self):
        return self.name