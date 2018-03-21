from django.contrib import admin
from studeals.models import Category, Offer, Comment, Vote
from studeals.models import UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass




admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Vote)
