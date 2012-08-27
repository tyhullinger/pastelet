from django.db import models
from django.forms import ModelForm, Textarea, Select
from django.db.models.signals import pre_save

from pygments.lexers import get_all_lexers

import random
import string

class Pastelet(models.Model):
    #id = models.CharField(max_length=256, primary_key=True)
    url = models.CharField(max_length=256, blank = True)
    name = models.CharField(max_length=75, blank = True, null=True)
    language = models.CharField(max_length=75)
    code = models.TextField()
    created = models.TimeField(auto_now=True)

    def __unicode__(self):
        return self.id

class PasteletForm(ModelForm):
    fields = ('name', 'language', 'code')
    widgets = {
            'code': Textarea(attrs={'cols': 80, 'rows': 20})
    }
    class Meta:
        model = Pastelet

    def clean_url(self):
        data = self.cleaned_data['url']
        if data == '':
            data = url_generator()
        return data

    def clean_name(self):
        data = self.cleaned_data['name']
        if data == '':
            data = 'Anonymous'
        return data

def pastelet_save_handler(sender, **kwargs):
    sender.url = url_generator()

def url_generator():
    random_chars = string.ascii_uppercase + string.digits
    return ''.join(random.sample(random_chars, 15))

pre_save.connect(pastelet_save_handler)
