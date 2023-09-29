from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# from ckeditor.fields import RichTextField
from PIL import Image


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='default.jpg',
        upload_to='profile_images'
        )
    bio = models.TextField()

    def save(self, *args, **kwargs):
        """Фото профиля пользователя"""

        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['user']

    def __str__(self):
        return self.user.username


class Country(models.Model):
    """Модель страны"""

    name = models.CharField(max_length=150, default=None, unique=True)
    image_flag = models.ImageField(
        default='default_flag.jpg',
        upload_to='country_flags'
        )
    description = models.TextField(blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=50, blank=True)
    image_country = models.ImageField(
        default='default_country.jpg',
        upload_to='country_image'
        )

    def save_flag(self, *args, **kwargs):
        """Сохранение флага страны"""

        super().save()
        img = Image.open(self.image_flag.path)
        if img.height > 350 or img.width > 550:
            new_img = (550, 350)
            img.thumbnail(new_img)
            img.save(self.image_flag.path)

    def save(self, *args, **kwargs):
        """Сохранение изображения страны"""

        super().save()
        img = Image.open(self.image_country.path)
        if img.height > 400 or img.width > 600:
            new_img = (600, 400)
            img.thumbnail(new_img)
            img.save(self.image_country.path)

    def __str__(self):
        return self.name


class MountainRange(models.Model):
    """Модель горного массива"""

    name = models.CharField(max_length=150, default=None, unique=True,)

    def __str__(self):
        return self.name


class AboutSummit(models.Model):
    """Информация о вершине"""

    title = models.CharField(verbose_name='Name of mountain', max_length=200,
                             default=None, unique=True,)
    high = models.PositiveIntegerField(default=0)
    description = models.TextField(default=None)
    long_pos = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
        )
    lat_pos = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
        )
    country = models.ForeignKey(
        Country,
        verbose_name='First Country',
        on_delete=models.CASCADE,
        related_name='country_first'
        )
    country_2 = models.ForeignKey(
        Country,
        verbose_name='Second country',
        on_delete=models.CASCADE,
        related_name='country_second',
        blank=True,
        null=True
        )
    mountainrange = models.ForeignKey(
        MountainRange,
        on_delete=models.CASCADE
    )
    image_prev = models.FileField(
        upload_to='images/prev/%Y-%m-%d/',
        default='mountain-default.jpg'
        )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        )

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image_prev.path)
        if img.height > 400 or img.width > 600:
            new_img = (600, 400)
            img.thumbnail(new_img)
            img.save(self.image_prev.path)

    def __str__(self):
        return self.title


class MountainImages(models.Model):
    """Изображения к вершине, основные"""

    aboutsummit = models.ForeignKey(
        AboutSummit,
        default=None,
        on_delete=models.CASCADE
        )
    images = models.FileField(upload_to='images/')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.images.path)
        if img.height > 1080 or img.width > 1920:
            new_img = (1920, 1080)
            img.thumbnail(new_img)
            img.save(self.images.path)

    def __str__(self):
        return self.aboutsummit.title


class Post(models.Model):
    title = models.CharField(
        'Заголовок записи',
        max_length=200,
    )
    text = HTMLField(
        verbose_name='Текст',
        help_text='Текст вашего отчета',
    )
    # text = RichTextField(
    #    verbose_name='Текст',
    #    help_text='Текст вашего отчета',
    # )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    summit_select = models.ForeignKey(
            AboutSummit,
            blank=True,
            null=True,
            related_name='posts',
            verbose_name='Гора',
            help_text='Отчет к какой вершине вы пишите',
            on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчет'

    def __str__(self):
        return self.title[:15]
