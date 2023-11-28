from django import forms
from .models import Record  # Import your Record model

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['person', 'section', 'car', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        # Sort the person choices alphabetically
        self.fields['person'].queryset = self.fields['person'].queryset.order_by('login')
