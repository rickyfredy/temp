import datetime

from django.db import models


class Author(models.Model):
    author_name = models.CharField(max_length=200)
    def __str__(self):
        return self.author_name