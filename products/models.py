from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Categories' # renames the categorys to categories in admin section of the app
        ordering = ('name',) # orders alphabetically

    def __str__(self): # overwrites the name given in line 4
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(283,158)],
                                     options={'quality': 90})
    is_sold = models.BooleanField(default=False) # default the item to be marked as not sold
    create_date = models.DateField(auto_now_add=True) # automatically adds in the date when its created
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def __str__(self): # overwrites the name given in line 16
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image)
        width, height = img.size
        target_width = 600
        h_coefficient = width/600
        target_height = height/h_coefficient
        img = img.resize((int(target_width), int(600)), Image.ANTIALIAS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()

    

