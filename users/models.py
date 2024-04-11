from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=4, blank=False)
    country = models.CharField(max_length=30, blank=True)
    address1 = models.TextField(max_length=100, blank=True)
    address2 = models.TextField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=30, blank=True)
    phone = models.IntegerField(null=True)
    full_name = models.CharField(max_length=64, blank=True)
    image = models.ImageField(default='profile_images/default.jpg', upload_to='profile_images', blank=True)

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image)
        width, height = img.size
        target_width = 300
        h_coefficient = width/300
        target_height = height/h_coefficient
        img = img.resize((int(target_width), int(300)), Image.ANTIALIAS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()