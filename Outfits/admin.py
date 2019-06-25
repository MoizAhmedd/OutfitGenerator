from django.contrib import admin
from .models import ClothingItem, BadOutfit, AnticipatedItem
# Register your models here.
admin.site.register(ClothingItem)
admin.site.register(BadOutfit)
admin.site.register(AnticipatedItem)
