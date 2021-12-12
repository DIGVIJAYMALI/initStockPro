from django.db import models

#basically it is a table
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
	
    def __unicode__(self):
        return self.username		