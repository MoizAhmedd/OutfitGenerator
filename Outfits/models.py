from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from . import generate
from . import storage
from PIL import Image
import os

# Create your models here.
class ClothingItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

    def __str__(self):
        return "{}'s {}".format(self.user.username,self.name)
    
    def get_absolute_url(self):
        return reverse('dashboard',kwargs = {style:0})
    
    def save(self):
        super().save()

        #Create Product
        project_id = "outfitgenerator"
        location =  "us-east1"
        product_id = self.user.username + "_" + str(self.id)
        product_set_id = self.user.username + "_PS"
        product_display_name = self.name
        product_category = "apparel"
        key = "category"
        value = self.category
        generate.create_product(project_id,location,product_id,product_display_name,product_category)

        #Add Product to Product Set
        generate.add_product_to_product_set(project_id,location,product_id,product_set_id)

        #Add product labels
        generate.update_product_labels(project_id,location,product_id,key,value)

        #Upload image to storage
        path = self.image.path 
        bucket = "clothmatching"
        file_name = self.name.replace(" ","") + str(self.id)
        storage.upload_blob(bucket,path,file_name)

        #Create Reference Image
        ref_id = "REFIMAGE-" + str(self.id)
        uri = "gs://clothmatching/" + file_name
        generate.create_reference_image(project_id,location,product_id,ref_id,uri)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        

class BadOutfit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    items = models.ManyToManyField(ClothingItem)

    def __str__(self):
        return "Outfit:{}, Disliked by {}".format(self.id,self.user)


class PossibleItem(models.Model):
    category = models.CharField(max_length = 20,default='upper')
    name = models.CharField(max_length = 100,default='shirt')
    image = models.ImageField(default='default.jpg',upload_to='clothes_pics')

    def __str__(self):
        return "{}".format(self.name)
    
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class StyleOne(models.Model):
    #Alex Costa Youtube Channel
    season = models.CharField(max_length = 20)
    items = models.ManyToManyField(PossibleItem)
    
    def __str__(self):
        return "Alex Costa outfit #{}".format(self.id)

class StyleTwo(models.Model):
    #AlphaM Youtube Channel
    season = models.CharField(max_length = 20)
    items = models.ManyToManyField(PossibleItem)
    
    def __str__(self):
        return "AlphaM outfit #{}".format(self.id)

class StyleThree(models.Model):
    #TMF Youtube Channel
    season = models.CharField(max_length = 20)
    items = models.ManyToManyField(PossibleItem)
    
    def __str__(self):
        return "TMF outfit #{}".format(self.id)