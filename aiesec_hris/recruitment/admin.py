from django.contrib import admin

# Register your models here.
from .models import Applicant, Timeline

admin.site.register(Applicant)
admin.site.register(Timeline)
