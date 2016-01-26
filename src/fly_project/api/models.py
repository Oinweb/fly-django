import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# http://stackoverflow.com/questions/14838128/django-rest-framework-token-authentication


class BannedDomain(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'fly_banned_domains'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)


class BannedIP(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('address',)
        db_table = 'fly_banned_ips'
    
    id = models.AutoField(primary_key=True)
    address = models.GenericIPAddressField(db_index=True, unique=True)
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.address)


class BannedWord(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('text',)
        db_table = 'fly_banned_words'
    
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.text)


class ImageUpload(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('upload_date',)
        db_table = 'fly_image_uploads'
    
    upload_id = models.AutoField(primary_key=True)
    upload_date = models.DateField(auto_now=True, null=True)
    image = models.ImageField(upload_to='upload', null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True,)
    
    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(ImageUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
    
    def __str__(self):
        return str(self.upload_id)
