from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        slug_exists = True
        counter = 2
        self.slug = slug
        while slug_exists:
            try:
                cat = Category.objects.get(slug=self.slug)
                if cat == self:
                    slug_exists = False
                    break
                self.slug = slug + '-' + str(counter)
                counter += 1
            except Category.DoesNotExist:
                slug_exists = False
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='media/profile_images')

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

class Offer(models.Model):
    category = models.ForeignKey(Category)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=20)
    promotion = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    place_latitude = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    place_longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    place_address = models.CharField(max_length=200)
    place_name = models.CharField(max_length=30)
    expiration_date = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        """ Saving model with slug field """
        slug = slugify(self.title)
        slug_exists = True
        counter = 2
        self.slug = slug
        while slug_exists:
            try:
                offer = Offer.objects.get(slug=self.slug)
                if offer == self:
                    slug_exists = False
                    break
                self.slug = slug + '-' + str(counter)
                counter += 1
            except Offer.DoesNotExist:
                slug_exists = False
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " commented " + self.offer + " with : " + self.comment

class Vote(models.Model):
    vote = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " voted " + self.vote + " on " + self.offer
