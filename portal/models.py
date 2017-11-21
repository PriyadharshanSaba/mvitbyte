# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class TeachaProfile(models.Model):
    name = models.CharField(max_length = 45)
    notes = models.FileField()
#(upload_to='', blank=True)
#enctype="multipart/form-data
