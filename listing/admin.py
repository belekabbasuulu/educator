from django.contrib import admin
from .models import Listing, Categories

admin.site.register(Categories)
admin.site.register(Listing)

