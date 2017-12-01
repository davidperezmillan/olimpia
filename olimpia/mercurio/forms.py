from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Series


CHOICES = (( False,'No',), ( True,'Si',))
CHOICES_QUALITY = (( 'NR','NR',),( 'HD','HD',),( 'VO','VO',),)

class SeriesForm(forms.ModelForm):
    
    ep_start = forms.CharField(max_length=8, min_length=8,  initial="NRS00E00",widget=forms.TextInput(attrs={'class' : 'form-control'}))
    ep_end = forms.CharField(max_length=8, min_length=8,  initial="NRS99E99",widget=forms.TextInput(attrs={'class' : 'form-control'}))
    quality = forms.CharField(max_length=2, min_length=2,  initial="NR",widget=forms.Select(attrs={'class' : 'form-control'},choices=CHOICES_QUALITY))
    
    
    class Meta:
        model = Series
        fields = ('nombre', 'quality','ep_start','ep_end','paussed', 'skipped',  )
        widgets = {
            'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
            'paussed': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
            'skipped': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
          
      }
        
        
        