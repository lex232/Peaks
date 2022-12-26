from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# resizing images


# Расширяем поля для пользователя One-To-One
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.username

# Страны Many-to-One
class Country(models.Model):
    name = models.CharField(max_length=150, default = None)

    def __str__(self):
        return self.name

# Горный массив Many-to-One
class MountainRange(models.Model):
    name = models.CharField(max_length=150, default = None)

    def __str__(self):
        return self.name



# БД о вершине, информация self
class AboutSummit(models.Model):
    title = models.CharField(max_length=200, default = None)
    high = models.PositiveIntegerField(default = 0)
    description = models.TextField(default = None)
    #Координаты
    long_pos = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lat_pos = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    #Страна и Горный массив.
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    mountainrange = models.ForeignKey(MountainRange, on_delete=models.CASCADE)
    #Изображение - превью
    image_prev = models.FileField(upload_to = 'images/', default='mountain-default.jpg')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image_prev.path)
        if img.height > 200 or img.width > 300:
            new_img = (300, 200)
            img.thumbnail(new_img)
            img.save(self.image_prev.path)

    def __str__(self):
        return self.title

class MountainImages(models.Model):
    aboutsummit = models.ForeignKey(AboutSummit, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.images.path)
        if img.height > 1080 or img.width > 1920:
            new_img = (1920, 1080)
            img.thumbnail(new_img)
            img.save(self.images.path)

    def __str__(self):
        return self.aboutsummit.title