from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ClothingItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

    def __str__(self):
        return "{}'s {}".format(self.user.username,self.name)
    


