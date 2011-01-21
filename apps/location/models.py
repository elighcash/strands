from django.db import models

class Location(models.Model):
    """
    None of the fields are required, so a location can be just geo coordinates, just a name, or any combination of fields.
    """
    
    name = models.CharField(max_length=255, blank=True, help_text="Location name.")
    address = models.CharField(max_length=255, blank=True, help_text="Location address.")
    city = models.CharField(max_length=255, blank=True, help_text="City.")
    region = models.CharField(max_length=255, blank=True, help_text="Region.")
    postal_code = models.CharField(max_length=255, blank=True, help_text="Postal code.")
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
