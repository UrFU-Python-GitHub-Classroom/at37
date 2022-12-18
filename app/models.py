from django.db import models

class Profession(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to="images/", verbose_name='Фото')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


class Statistic(models.Model):
    title = models.CharField('Название', max_length=50)
    image = models.ImageField(upload_to="images/", verbose_name='График')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'