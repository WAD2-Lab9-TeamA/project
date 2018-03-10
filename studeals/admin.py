from django.contrib import admin
from studeals.models import Category, Offer, Comment, Vote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment)
admin.site.register(Vote)
