from django import forms  # Import Django's forms module
from .models import Study  # Import the Study model from your models

# Create a ModelForm for the Study model
class StudyForm(forms.ModelForm):
    class Meta:
        model = Study  # Specify which model the form is based on
        fields = ['name', 'phase', 'sponsor', 'description']  # Specify the fields to include in the form
