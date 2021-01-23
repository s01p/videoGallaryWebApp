from django.db import models
from django.utils import timezone
from django.core.files import File
from urllib import request
import os

#import request
from io import BytesIO


class Photo(models.Model):
    tag = models.CharField(max_length=200)
    
    
    
class Photoa(models.Model):
    name = models.CharField(max_length=200)
    img = models.FileField(upload_to='images/')
    url_img = models.URLField(max_length=200)
    