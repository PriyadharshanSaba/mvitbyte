# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django import forms

# Create your tests here.


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
