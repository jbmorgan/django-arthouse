from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location=settings.MEDIA_ROOT)

class UserProfile(models.Model):
    """
    Not currently used in the system.  Will most likely be removed when django
    1.5 is available.
    """
    # This field is required.
    user = models.OneToOneField(User)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Movie(models.Model):
    """
    A ``Movie`` is a collection of all the information needed to uniquely
    identify, schedule, and promote a movie or special event.
    """
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies' 

    FILM_RATINGS = (
        ('G',       'G'),
        ('PG',      'PG'),
        ('PG13',    'PG-13'),
        ('R',       'R'),
        ('NC17',    'NC-17'),
        ('NR',      'Not Rated'),
    )

    title           = models.CharField(max_length=200)
    tmdb_id         = models.CharField(max_length=64)
    description     = models.TextField(u'description')
    slug            = models.SlugField()
    genres          = models.CharField(max_length=200)

    length          = models.IntegerField()
    year            = models.IntegerField()
    rating          = models.CharField(max_length=12)
    languages       = models.CharField(max_length=200)

    directors       = models.CharField(max_length=512)
    writers         = models.CharField(max_length=512)
    cast            = models.CharField(max_length=512)

    poster_image    = models.ImageField(    u'poster image', 
                                            upload_to='posters', 
                                            storage=fs, 
                                            blank=True, 
                                            null=True)

    banner_image    = models.ImageField(    u'banner image', 
                                            upload_to='banners', 
                                            storage=fs, 
                                            blank=True, 
                                            null=True)
    tile_image      = models.ImageField(    u'tile image', 
                                            upload_to='tiles', 
                                            storage=fs, 
                                            blank=True, 
                                            null=True)
    site_url        = models.URLField()
    imdb_url        = models.URLField()

    def __unicode__(self):
        return u'%s (%i)' % (self.title, self.year)

    def poster_url(self):
        return '/media/%s' % self.poster_image.url 
        
    def banner_url(self):
        return '/media/%s' % self.banner_image.url 
    
    def tile_url(self):
        return '/media/%s' % self.tile_image.url    

    @models.permalink
    def get_absolute_url(self):
        return ('arthouse:movie_detail_url', [self.pk])


class Theater(models.Model):
    """
    A ``Theater`` is a particular screening room at a cinema location where 
    movies and special events can take place. ``Theater``s are primarily used
    for scheduling ``Showtime``s.
    """
    class Meta:
        verbose_name = 'Theater'
        verbose_name_plural = 'Theaters' 

    name        = models.CharField(max_length=32)

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('arthouse:movie_detail_url', [self.pk])


class TicketType(models.Model):
    """
    A ``TicketType`` is generally one of many types of tickets available for a 
    ``PriceSheet``.
    """
    class Meta:
        verbose_name = 'Ticket Type'
        verbose_name_plural = 'Ticket Types' 

    name        = models.CharField(max_length=32)
    price       = models.DecimalField(max_digits=5, decimal_places=2)
    allow_comp  = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.name)


class PriceSheet(models.Model):
    """
    A ``PriceSheet`` contains the ``TicketType``s and prices per ticket type for 
    a film or special event. While some screenings, especially special events,
    may have unique price sheets, most screenings will share one of a handful
    of ``PriceSheet``s (all regularly priced matinee shows, for example, would
    generally share the same ``PriceSheet``).
    """
    class Meta:
        verbose_name = 'Price Sheet'
        verbose_name_plural = 'Price Sheets' 

    name        = models.CharField(max_length=64)
    ticket_types = models.ManyToManyField(TicketType)

    def __unicode__(self):
        return unicode(self.name)


class Showtime(models.Model):
    """
    A ``Showtime`` represents a particular date and time that a film or event
    is playing, along with the associated rules and ticket prices.
    """
    class Meta:
        verbose_name = 'Showtime'
        verbose_name_plural = 'Showtimes' 

    movie           = models.ForeignKey(Movie)
    time            = models.DateTimeField()
    price_sheet     = models.ForeignKey(PriceSheet)
    accept_passes   = models.BooleanField()

    def __unicode__(self):
        return unicode(self.time)


