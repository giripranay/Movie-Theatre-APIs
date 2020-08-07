# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Screen,Row,Seat

admin.site.register(Screen)
admin.site.register(Row)
admin.site.register(Seat)