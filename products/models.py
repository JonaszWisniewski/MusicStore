from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from djmoney.models.fields import MoneyField


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
    price = MoneyField(max_digits=6, default = 50.00, decimal_places=2, default_currency='USD')
    rating = models.PositiveIntegerField(default=1, null=True, blank=True, choices=((1, '1 star'), (2, '2 star'), (3, '3 star'), (4, '4 star'), (5, '5 star')))
    image = models.ImageField(default='product_images/default_image.png', upload_to='product_images', blank=True, null=True)
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


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    

