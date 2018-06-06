from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

# Create your models here.


class Sport(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, max_length=200)
    thumbnail=models.ImageField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Sport, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()
    status=models.CharField(max_length=200, choices=(('submitted', 'submitted'),
                                                     ('approved', 'approved'), ('rejected','rejected')))
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    sport=models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    tags=TaggableManager()
    slug = models.SlugField(null=True, blank=True, max_length=200)
    created_date=models.DateTimeField(auto_now_add=True, null=True)
    approved_date=models.DateTimeField(null=True)
    online=models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


