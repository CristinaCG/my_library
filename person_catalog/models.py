from django.db import models
# from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

class Person(models.Model):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    birth_year = models.IntegerField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, null=True, blank=True)
    death_date = models.IntegerField(null=True, blank=True)
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name[0]}. {self.last_name}'


