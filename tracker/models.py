from django.db import models

class Milestone(models.Model):
    # The title of what you achieved (e.g., "Learned JavaScript")
    title = models.CharField(max_length=200)
    
    # Category helps you filter between Backend, Cyber, or Hub Events
    category = models.CharField(max_length=50) 
    
    # A place to write details about what you did
    description = models.TextField()
    
    # Automatically records the date you added it
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title