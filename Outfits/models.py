from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.
class ClothingItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #user = request.user
    category = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

    def __str__(self):
        return "{}'s {}".format(self.user.username,self.name)
    
    def get_absolute_url(self):
        return reverse('dashboard')
    
    def save(self):
        print(self.image)
        super().save()
        #print(self.category)
        #user = request.user
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        

class BadOutfit(models.Model):
    items = models.ManyToManyField(ClothingItem)

    def __str__(self):
        return "{}".format(self.items)

class AnticipatedItem(ClothingItem):
    user = None
    name = models.CharField(max_Length = 100)

    def __str__(self):
        return "{}".format(self.name)
    

