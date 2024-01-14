from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    year = models.IntegerField()
    synopsis = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
