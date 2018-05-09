from django import forms

from .models import Document, Ficha, Descarga


class FichaModelForm(forms.ModelForm):



    class Meta:
        model = Ficha
        fields = ('nombre','estado')
        # widgets = { }



class DescargaModelForm(forms.ModelForm):
    '''
    ficha = models.OneToOneField(Ficha)
    ep_start = models.CharField(max_length=8, default='NRS00E00',blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ep_end = models.CharField(max_length=8, default='NRS99E99', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    quality = models.CharField(max_length=2, choices=choice_quality, blank=False, null=False)  # Field name made lowercase. This field type is a guess.
    ultima = models.DateTimeField(blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    estado_descarga = models.NullBooleanField(default=False)  # Field name made lowercase.
    plugins = models.ManyToManyField(Plugin, blank=True)
    '''


    class Meta:
        model = Descarga
        fields = ('ficha','ep_start','ep_end', 'quality', 'plugins', 'estado_descarga')
        # widgets = { }






class UploadFileForm(forms.ModelForm):
    filename = forms.CharField(max_length=100, label="Nombre del documento")
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )
    
    class Meta:
        model = Document
        fields = ('ficha', 'filename','docfile')
        # widgets = { }
    
 