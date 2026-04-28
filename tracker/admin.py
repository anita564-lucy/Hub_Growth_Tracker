from django.contrib import admin
from .models import Milestone

# This tells Django to show your Milestone model in the admin site
admin.site.register(Milestone)