from django.contrib import admin
from .models import ClothingItem, BadOutfit,PossibleItem, StyleOne, StyleTwo, StyleThree
# Register your models here.
admin.site.register(ClothingItem)
admin.site.register(BadOutfit)
admin.site.register(PossibleItem)
admin.site.register(StyleOne)
admin.site.register(StyleTwo)
admin.site.register(StyleThree)

