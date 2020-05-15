from django.db import models
from ..user_resume.models import Resume

class ResumeItem(models.Model):
    """
    A single resume item, representing a job and title held over a given period
    of time.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    title = models.CharField(max_length=127)
    company = models.CharField(max_length=127)

    start_date = models.DateField()
    # Null end date indicates position is currently held
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=2047, blank=True)
    
    parent_resume_id = models.PositiveIntegerField(default=-1)
    
    def __unicode__(self):
        return "{}: ResumeID:{}, {} at {} ({})"\
            .format(self.user.username,
                    self.title,
                    self.company,
                    self.start_date.isoformat())
        
    def __str__(self):
        return "{}: ResumeID:{}, {} at {} ({})"\
            .format(self.user.username,
                    self.title,
                    self.company,
                    self.start_date.isoformat())
