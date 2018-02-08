from django import forms

from .models import Document


class UploadFileForm(forms.ModelForm):
    filename = forms.CharField(max_length=100, label="Nombre del documento")
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )
    
    class Meta:
        model = Document
        fields = ('ficha', 'filename','docfile')
        # widgets = { }
    
 