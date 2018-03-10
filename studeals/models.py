from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=20)
    price = models.IntegerField(blank=True)
    description = models.CharField(max_length=200)
    place_address = models.CharField(max_length=200)
    place_name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='offers', blank=True)
    expiration_date = models.DateField()
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " commented " + self.offer + " with : " + self.comment

class Vote(models.Model):
    vote = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " voted " + self.vote + " on " + self.offer
