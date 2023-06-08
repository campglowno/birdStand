from django.db import models

BIRD_LIST = (
    (1, 'pustółka'),
    (2, 'drozd'),
    (3, 'czyżyk'),
    (4, 'rudzik'),
    (5, 'sroka'),
    (6, 'wróbel'),
    (7, 'kruk')
)


class Place(models.Model):
    name = models.CharField(max_length=64, verbose_name='miejsce')
    city = models.CharField(max_length=64, verbose_name='miasto', null=True)
    country = models.CharField(max_length=64, verbose_name='kraj')

    def __str__(self):
        return f'{self.name} - {self.city}, {self.country}'


class Watcher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    places = models.ManyToManyField(Place, through='BirdStand')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Bird(models.Model):
    name = models.CharField(max_length=64, verbose_name='nazwa')
    scientific_name = models.CharField(max_length=64, verbose_name='nazwa naukowa')
    weight = models.IntegerField(null=True, blank=True, verbose_name='waga [g]')
    length = models.IntegerField(null=True, blank=True, verbose_name='długość [cm]')
    species = models.CharField(max_length=64, blank=True, verbose_name='gatunek')

    def __str__(self):
        return f'{self.name}'


class BirdStand(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    watcher = models.ForeignKey(Watcher, on_delete=models.CASCADE)


class BirdPhoto(models.Model):
    image = models.ImageField(upload_to='static/')
    name = models.ForeignKey(Bird, on_delete=models.CASCADE)
