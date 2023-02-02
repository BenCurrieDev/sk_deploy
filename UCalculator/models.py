from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=30, unique=True)
    thermal_conductivity = models.FloatField()
    color = models.CharField(max_length=30, default="grey")
    def __str__(self):
        return self.name

class Composite(models.Model):
    name = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def calcThickness(self):
        components = self.component_set.all()
        thicknesses = [component.thickness for component in components]
        return sum(thicknesses)

    def calcU(self):
        components = self.component_set.all()
        if components:
            Rs = [component.calcR() for component in components]
            return round(1/(0.13 + sum(Rs) + 0.04), 2)
        else:
            return 'N/A'

    def __str__(self):
        return self.name

class Component(models.Model):
    thickness = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    composite = models.ForeignKey(Composite, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def calcR(self):
        return ((self.thickness * 0.001) / self.material.thermal_conductivity)
    
    def displayR(self):
        return round((self.thickness * 0.001) / self.material.thermal_conductivity, 2)

    def __str__(self):
        return self.material.name + ' (' + str(self.thickness) + 'mm)'

