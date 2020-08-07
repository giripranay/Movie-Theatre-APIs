# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models

# Create your models here.
class Screen(models.Model):
    screen_name = models.CharField(max_length = 30, unique = True, blank = False)

class Row(models.Model):
    screen = models.ForeignKey(Screen, on_delete = models.CASCADE)
    row_name = models.CharField(max_length = 5,blank = False)
    number_of_seats = models.IntegerField()
    aisle_seats = models.CharField(max_length = 30)

class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete = models.CASCADE)
    row = models.ForeignKey(Row, on_delete = models.CASCADE)
    seat_number = models.IntegerField(blank = False)
    is_reserved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('screen','row','seat_number')
        