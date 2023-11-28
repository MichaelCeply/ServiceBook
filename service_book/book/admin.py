from django.contrib import admin
from .models import Person, Section,Car,Record

# Register your models here.
admin.site.register(Person)
admin.site.register(Section)
admin.site.register(Car)
admin.site.register(Record)