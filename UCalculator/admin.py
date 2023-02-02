from django.contrib import admin
from .models import Material, Component, Composite

# Register your models here.
admin.site.register(Material)
admin.site.register(Component)
admin.site.register(Composite)