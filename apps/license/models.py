from django.db import models

# META INFORMATION
#####################################################################
class License(models.Model):
    """
    License class allows specific licenses to be defined site-wide,
    which can then be applied to knots when posted. The knot's
    license info is automatically rendered in the template, so that
    it's searchable.
    
    """
    
    name = models.CharField(max_length=100, blank=True, help_text="License name (e.g. Creative Commons Attribution-Share Alike).")
    abbreviation = models.CharField(max_length=200, blank=True, help_text="License abbreviation (e.g. CC BY-SA).")
    description = models.TextField(blank=True, help_text="License description.")
    code_url = models.URLField(blank=True, help_text="URL of license code.") #prefer url?
    code = models.TextField(blank=True, help_text="License code.")

    def __unicode__(self):
        return self.name