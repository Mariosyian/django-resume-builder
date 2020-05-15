from django.db import models
from datetime import datetime

class Resume(models.Model):
    """
    A single resume, represents an object that holds resume items.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    num_items = models.PositiveSmallIntegerField()

    # How to be displayed when viewed using the shell
    def __str__(self):
        return "{}: {}, has {} items".format(self.user,
                                             self.name,
                                             self.num_items)