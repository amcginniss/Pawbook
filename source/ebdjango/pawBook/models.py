from django.db import models

# Create your models here.

class SocialPost(models.Model):
   usern = models.CharField(max_length=100)
   title = models.CharField(max_length=40)
   content = models.TextField()

CITIES = (
   ('melbourne','Melbourne'),
   ('sydney','Sydney'),
   ('brisbane','Brisbane'),
   ('darwin','Darwin'),
   ('perth','Perth'),
   ('adelaide','Adelaide'),
   ('hobart','Hobart'),
)

class WeatherPost(models.Model):
   usern = models.CharField(max_length=100)
   title = models.CharField(max_length=40)
   location = models.CharField(max_length=9, choices=CITIES,default='melbourne')

class DogPost(models.Model):
   usern = models.CharField(max_length=100)
   title = models.CharField(max_length=40)
   imgUrl = models.CharField(max_length=100)
   content = models.TextField()