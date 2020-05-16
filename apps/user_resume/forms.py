from django import forms

from .models import Resume

class CreateResumeForm(forms.ModelForm):
    """
    A form for creating a new user resume. Note that:
    'user' is always set to the requesting user.
    'num_items': defaults to 0.
    'date_created': gets the current time of creation.
    'date_modified': gets the current time of update.
    """
    class Meta:
        model = Resume
        fields = ['name']
