from django import forms

from .models import Resume


class CreateResumeForm(forms.ModelForm):
    """
    A form for creating a new user resume. Note that 'user' is not
    included: it is always set to the requesting user. As well as
    the number of items is not included: defaults to 0.
    """
    class Meta:
        model = Resume
        fields = ['name']
