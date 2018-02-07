from django import forms

class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=100)
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )